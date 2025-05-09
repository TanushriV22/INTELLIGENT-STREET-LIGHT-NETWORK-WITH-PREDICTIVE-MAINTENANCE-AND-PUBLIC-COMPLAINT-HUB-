from app import create_app

app = create_app()

if __name__ == '__main__':
    print("="*80)
    print("Streetlight Complaint Management System")
    print("="*80)
    print("Server is running at: http://localhost:8080")
    print("You can access the website by opening a browser and navigating to:")
    print("http://localhost:8080")
    print("\nLogin credentials:")
    print("Admin: admin@example.com / admin123")
    print("User: user@example.com / user123")
    print("="*80)
    app.run(debug=True, port=8080)
