from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from database import db
import os
from controllers.don_hang_controller import handle_connect, handle_disconnect, handle_join
from controllers.binh_luan_controller import handle_connect_binh_luan, handle_disconnect_binh_luan, handle_join_binh_luan
from routes.thong_bao_routes import thong_bao_bp

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/drink_shop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', 'hinh_anh')
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)
    socketio.init_app(app)

    from routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    from routes.admin_user_routes import admin_user_bp
    app.register_blueprint(admin_user_bp, url_prefix='/api/admin')

    from routes.danh_muc_routes import danh_muc_bp
    app.register_blueprint(danh_muc_bp, url_prefix='/api/danh-muc')

    from routes.do_uong_routes import do_uong_bp
    app.register_blueprint(do_uong_bp, url_prefix='/api/do-uong')

    from routes.gio_hang_routes import gio_hang_bp
    app.register_blueprint(gio_hang_bp, url_prefix='/api/gio-hang')

    from routes.don_hang_routes import don_hang_bp
    app.register_blueprint(don_hang_bp, url_prefix='/api/don-hang')

    from routes.tuy_chon_routes import tuy_chon_bp
    app.register_blueprint(tuy_chon_bp, url_prefix='/api/tuy-chon')

    from routes.thong_bao_routes import thong_bao_bp
    app.register_blueprint(thong_bao_bp, url_prefix='/api/thong-bao')

    from routes.binh_luan_routes import binh_luan_bp
    app.register_blueprint(binh_luan_bp, url_prefix='/api/binh-luan')

    from routes.contact_routes import lien_he_bp
    app.register_blueprint(lien_he_bp, url_prefix = '/api/lien-he')

    from routes.blog_routes import blog_bp
    app.register_blueprint(blog_bp,url_prefix = '/api/blog')

    @app.route('/uploads/hinh_anh/<filename>')
    def serve_uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    socketio.on_event('connect', handle_connect, namespace='/don-hang')
    socketio.on_event('disconnect', handle_disconnect, namespace='/don-hang')
    socketio.on_event('join', handle_join, namespace='/don-hang')
    socketio.on_event('connect', handle_connect, namespace='/thong-bao')
    socketio.on_event('disconnect', handle_disconnect, namespace='/thong-bao')
    socketio.on_event('join', handle_join, namespace='/thong-bao')
    socketio.on_event('connect', handle_connect_binh_luan, namespace='/binh-luan')
    socketio.on_event('disconnect', handle_disconnect_binh_luan, namespace='/binh-luan')
    socketio.on_event('join', handle_join_binh_luan, namespace='/binh-luan')

    return app