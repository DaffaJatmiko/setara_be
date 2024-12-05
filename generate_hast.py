from passlib.context import CryptContext

# Konfigurasi hashing bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    """
    Fungsi untuk meng-hash password menggunakan bcrypt.
    
    Args:
        password (str): Password yang akan di-hash.

    Returns:
        str: Password yang sudah di-hash.
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise ValueError(f"Error saat meng-hash password: {e}")

def main():
    """
    Fungsi utama untuk mengambil input dari terminal dan menghasilkan hash password.
    """
    import sys

    if len(sys.argv) != 2:
        print("Usage: python generate_hash.py <password>")
        sys.exit(1)

    password = sys.argv[1]

    if len(password) < 8:
        print("Error: Password harus memiliki panjang minimal 8 karakter.")
        sys.exit(1)

    try:
        hashed_password = generate_password_hash(password)
        print(f"Hashed Password: {hashed_password}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
