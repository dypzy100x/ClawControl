"""Verify Claw Control installation"""
import sys

def verify():
    print("🛡️ Verifying Claw Control installation...")
    
    try:
        import fastapi
        print("✅ FastAPI installed")
    except:
        print("❌ FastAPI missing")
        return False
    
    try:
        import psutil
        print("✅ psutil installed")
    except:
        print("❌ psutil missing")
        return False
    
    print("✅ All checks passed!")
    return True

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
