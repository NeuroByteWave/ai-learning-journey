def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

# Example usage
print("Temperature Converter")
choice = input("Convert from (C)elsius or (F)ahrenheit? ").lower()

if choice == "c":
    c = float(input("Enter temperature in Celsius: "))
    print("In Fahrenheit:", celsius_to_fahrenheit(c))
elif choice == "f":
    f = float(input("Enter temperature in Fahrenheit: "))
    print("In Celsius:", fahrenheit_to_celsius(f))
else:
    print("Invalid choice.")
