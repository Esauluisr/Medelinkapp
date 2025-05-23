# ------ Imports -----------
from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from ..models.models import db, Usuario, Foto, Diagnostico
from werkzeug.security import generate_password_hash, check_password_hash,os
from werkzeug.utils import secure_filename
from ..model_ia.cnn_model import load_and_predict


# ------ blueprint ---------
main = Blueprint('main', __name__)
login_manager = LoginManager()

# ------ login ---------

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@main.route('/',)
def inicio():
    return redirect(url_for('main.login'))

@main.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Error al iniciar sesión. Verifique su nombre de usuario y/o contraseña')
    return render_template('Login.html')


# ------ register ---------


@main.route('/RegistroDeUsuarios', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        edad = request.form.get('edad')
        genero = request.form.get('genero')
        password = request.form.get('password')
        cofimpassword = request.form.get('confirmpassword')
        
        if not genero:
            flash('Por favor, seleccione un género', 'error')
            return redirect(request.url)
        
        if password != cofimpassword:    
            flash('las contraseñas no coinciden')
            return redirect(url_for('main.RegistroDeUsuarios'))
        
        new_user = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            edad=int(edad),
            genero=genero,
            password=generate_password_hash(password)
        )
        
        db.session.add(new_user)
        db.session.flush()

        with open('backend/img/logo.png', 'rb') as f:
            img_bytes = f.read()
        
        
        fotop = Foto(nobrefoto='logo.png', imagen=img_bytes, usuario_id=new_user.id)
        db.session.add(fotop)
        db.session.commit()
        
        flash('Registro exitoso,por favor iniciar sesión')
        return redirect(url_for('main.login'))
    return render_template('RegistroDeUsuarios.html')


# ------ logaut ---------
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# ------ home ---------
@main.route('/home')
@login_required
def home():
    return render_template('home.html', email=current_user.email)


# ------ diagnostico ---------
# Directorio donde se guardarán las imágenes subidas

UPLOAD_FOLDER = 'frontend/static/uploads/' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','PNG', 'JPG', 'JPEG'}


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/Diagnostico', methods=['GET', 'POST'])
@login_required
def diagnostico():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash('No se encontro el archivo', 'error')
            return redirect(url_for('main.Diagnostico'))
        
        
        file = request.files['file']
        
        
        if file.filename == '':
            flash('No has seleccionado ningun archivo', 'error')
            return redirect(url_for('main.Diagnostico'))
        
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            #realizamos la prediccion
            prediction = load_and_predict(filepath)
            
            #guardamos la imagen en la base de datos
            nuevo_diagnostico = Diagnostico(
                nombrearchivo=filename,
                ruta=filepath,
                predicion=prediction,
                usuario_id=current_user.id
            )
            
            db.session.add(nuevo_diagnostico)
            db.session.commit()
            
            return render_template('Diagnostico.html', filename=filename, prediction=prediction)
    return render_template('Diagnostico.html')

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return url_for('static', filename='uploads/' + filename)


#----- historial ---------

@main.route('/Historial', methods=['GET', 'POST'])
@login_required
def historialmedico():
    
    
    diagnosticos = Diagnostico.query.filter_by(usuario_id=current_user.id).all()
    
    return render_template('Historial.html', diagnosticos=diagnosticos)


# ------ medidas de prevencion---------

@main.route('/Prevencion')
@login_required
def prevencion():
    return render_template('Prevencion.html')  


# ------ about ---------

@main.route('/Nosotros')
@login_required
def abaut():
    return render_template('Nosotros.html')

# ------ politica de privacidad---------

@main.route('/PoliticaDePrivacidad')
@login_required
def privacypolicy():
    return render_template('PoliticaDePrivacidad.html')


# ------ termsofuse ---------

@main.route('/TermosDeUso')
@login_required
def termsofuse():
    return render_template('TerminosDeUso.html')

# ------ myprofile ---------

@main.route('/Miperfil', methods=['GET', 'POST'])
@login_required
def myprofile():

    user = current_user
    
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('main.home'))

    return render_template('Miperfil.html', user=user)

# ------ editprofile ---------


@main.route('/foto/<int:id>')
@login_required
def verfoto(id):
    foto = Foto.query.get(id)
    return Response(foto.imagen, mimetype='image/jpeg')


@main.route('/editarusario', methods=['GET', 'POST'])
@login_required
def editarusario():

    
    user = current_user
        
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        
        file = None
        
        if 'file' in request.files:
            file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_bytes = file.read()
            
            # Actualiza la imagen del usuario
            foto = Foto.query.filter_by(usuario_id=Usuario.id).first() 
            
            # Si ya existe una foto, la actualizamos
            # Si no existe ninguna foto, agregamos una nueva
            if foto:  
                foto.nobrefoto = filename
                foto.imagen = img_bytes
            else: 
                foto = Foto(nobrefoto=filename, imagen=img_bytes, usuario_id=Usuario.id)
                db.session.add(foto)
                
            # Guarda los cambios
            db.session.commit()
            return redirect(url_for('main.editarusario'))
        
        # Actualiza los campos del usuario
        user.nombre = request.form.get('nombre')
        user.apellido = request.form.get('apellido')
        user.email = request.form.get('email')
        user.telefono = request.form.get('telefono')
        user.edad = request.form.get('edad')
        user.genero = request.form.get('genero')
        
        # Verifica si alguno de los campos requeridos está vacío
        if not user.nombre or not user.apellido or not user.email:
            flash('La accion no puede ser completada. Por favor, vulve a intentarlo')
            return redirect(url_for('main.editarusario'))

        # Actualiza los campos del usuario
        user.nombre = user.nombre
        user.apellido = user.apellido
        user.email = user.email
        user.telefono = user.telefono
        user.edad = user.edad
        user.genero = user.genero

        
        #guardar cambios 
        db.session.commit()
        return redirect(url_for('main.editarusario'))
    
    return render_template('EditarPerfil.html', user=user) 

# ------ changepassword ---------

@main.route('/CambiarContraseña', methods=['GET', 'POST'])
@login_required
def changepassword():
    
    user = current_user
    
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        
        # Imprime los valores para depuración
        print('password:', password)
        print('confirmpassword:', confirmpassword)
    
        # Verifica si alguno de los campos requeridos está vacío
        if not password or not confirmpassword:
            flash('Por favor, complete todos los campos requeridos.', 'error')
            return render_template('CambiarContraseña.html', user=user)
        
        # Verifica que las contraseñas coincidan
        if password != confirmpassword:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('CambiarContraseña.html', user=user)
        
        # Actualiza y encripta la nueva contraseña
        user.password = generate_password_hash(password)
        
        # Guarda los cambios en la base de datos
        db.session.commit()
        flash('Contraseña actualizada exitosamente , inicie sesión nuevamente')
        return redirect(url_for('main.login'))
    
    return render_template('CambiarContraseña.html', user=user)


# ------ deleteaccount ---------

@main.route('/EliminarCuenta', methods=["GET",'POST'])
@login_required
def deleteaccount():
    
    user =  current_user
    
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        # Eliminar los diagnosticos del usuario
        Diagnostico.query.filter_by(usuario_id=user.id).delete()

        # Eliminar el usuario de la base de datos
        db.session.delete(user)
        db.session.commit()

        logout_user()

        flash('Cuenta eliminada exitosamente')
        return redirect(url_for('main.login'))
    
    return render_template('EliminarCuenta.html', user=user)

