# Real-time Chat Application

A modern real-time chat application built with Flask, Socket.IO, and a clean responsive UI. Features include file sharing, real-time messaging, and user presence detection.

![Chat Application Screenshot](screenshots/chat-preview.png)

## Features

- 💬 Real-time messaging using WebSocket
- 📁 File sharing support (images, documents, PDFs)
- 👥 User presence detection
- 🎨 Modern, responsive UI with glass-morphism design
- 📱 Mobile-friendly interface
- 🔒 Production-ready setup with Gunicorn

## Technologies Used

- Backend:
  - Flask
  - Flask-SocketIO
  - Gunicorn (Production Server)
  - Eventlet (WebSocket Support)

- Frontend:
  - HTML5
  - CSS3 (Modern Features)
  - JavaScript (ES6+)
  - Socket.IO Client

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/chat-application.git
cd chat-application
```

2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
python app.py
```

### Production Mode
```bash
gunicorn --worker-class eventlet -w 1 wsgi:app
```

The application will be available at `http://localhost:5000`

## Project Structure

```
chat-application/
├── app.py              # Main Flask application
├── wsgi.py            # WSGI entry point
├── requirements.txt   # Python dependencies
├── Procfile          # Deployment configuration
├── static/           # Static files
│   └── b1.jpg       # Background image
├── templates/        # HTML templates
│   └── index.html   # Main chat interface
└── uploads/         # Uploaded files directory
```

## Features in Detail

1. **Real-time Messaging**
   - Instant message delivery
   - Message timestamps
   - User online status

2. **File Sharing**
   - Support for multiple file types
   - Preview icons for different file types
   - Secure file handling

3. **User Interface**
   - Glass-morphism design
   - Responsive layout
   - Dark/Light mode support
   - Smooth animations

## Deployment

The application is configured for deployment on various platforms:

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### PythonAnywhere
1. Create a PythonAnywhere account
2. Set up a new web app
3. Configure WSGI file to use `wsgi.py`
4. Set up virtual environment and install requirements

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Font Awesome for icons
- Google Fonts for the Inter font family