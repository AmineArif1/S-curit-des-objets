import binascii

def calculate_crc32(filename):
    try:
        with open(filename, 'rb') as f:
            buf = f.read()
        return binascii.crc32(buf)
    except FileNotFoundError:
        return "Le fichier n'a pas été trouvé."

# Utilisation de la fonction
filename = "T13.hex"  # Remplacez par le nom de votre fichier
print(f"CRC32: {calculate_crc32(filename):08X}")