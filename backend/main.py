from app import app

# Import service modules to register their routes on the shared app instance
import wishlist_service
import book_details_service
import login_service
import book_browsing

if __name__ == "__main__":
    app.run(debug=True)
