# Este programa funciona como calculadora para números complejos, tanto en forma polar rectangular como fasorial.
# Se presenta una interfaz gráfica que permite realizar las operaciones básicas de suma, resta, multiplicación, división y potencia.
# Los resultados se muestran en forma rectangular y fasorial, además se grafican los vectores en el plano complejo (operandos y resultado).
# Los operandos se pueden introducir en forma de números complejos o en forma de módulo y fase.

# Importación de librerías
import math
import tkinter as tk
import tkinter.simpledialog as simpledialog

import math

min_acceptable = 0.000000001

class Complejo:
    def __init__(self, real=None, imag=None, modulo=None, fase=None):
        assert (real!=None and imag!=None) or (modulo!=None and fase!=None), "Se debe introducir un número complejo en forma rectangular o polar"

        self.modulo = modulo if modulo!=None else math.sqrt(real**2 + imag**2)
        self.fase = fase if fase!=None else math.atan2(imag, real)

        # dejar la fase en el rango [-pi, pi]
        while self.fase > math.pi:
            self.fase -= 2 * math.pi
        while self.fase < -math.pi:
            self.fase += 2 * math.pi

        self.real = real if real!=None else modulo * math.cos(fase)
        self.imag = imag if imag!=None else modulo * math.sin(fase)

    def __str__(self):
        return f"{self.real} + {self.imag}i"
    
    def __repr__(self):
        return f"Complejo({self.real}, {self.imag})"
    
    def polar(self):
        return f"{self.modulo} ∠ {math.degrees(self.fase)}°"
    
    def rectangular(self):
        return f"{self.real} + {self.imag}i"
    
    def sumar(self, otro):
        return Complejo(self.real + otro.real, self.imag + otro.imag)
    
    def restar(self, otro):
        return Complejo(self.real - otro.real, self.imag - otro.imag)
    
    def multiplicar(self, otro):
        nuevo_modulo = self.modulo * otro.modulo
        nueva_fase = self.fase + otro.fase
        nuevo_real = nuevo_modulo * math.cos(nueva_fase)
        nuevo_imag = nuevo_modulo * math.sin(nueva_fase)
        return Complejo(nuevo_real, nuevo_imag, nuevo_modulo, nueva_fase)
    
    def dividir(self, otro):
        nuevo_modulo = self.modulo / otro.modulo
        nueva_fase = self.fase - otro.fase
        nuevo_real = nuevo_modulo * math.cos(nueva_fase)
        nuevo_imag = nuevo_modulo * math.sin(nueva_fase)
        return Complejo(nuevo_real, nuevo_imag, nuevo_modulo, nueva_fase)
    
    #def potencia(self, n):
    #    nuevo_modulo = self.modulo ** n
    #    nueva_fase = self.fase * n
    #    nuevo_real = nuevo_modulo * math.cos(nueva_fase)
    #    nuevo_imag = nuevo_modulo * math.sin(nueva_fase)
    #    return Complejo(nuevo_real, nuevo_imag, nuevo_modulo, nueva_fase)

class CalculadoraComplejos(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.crear_widgets()
        self.gl = {
            'math': math,
            'deg': math.degrees,
            'm': lambda x: x.modulo,
            'f': lambda x: math.degrees(x.fase),
            'r': lambda x: x.real,
            'i': lambda x: x.imag,
        }

    def crear_widgets(self):
        # Widgets número 1
        self.label_rectangular = tk.Label(self, text="Rectangular")
        self.label_rectangular.grid(row=0, column=1)

        self.label_polar = tk.Label(self, text="Polar")
        self.label_polar.grid(row=0, column=6)

        self.label1 = tk.Label(self, text="Número 1:", fg="blue")
        self.label1.grid(row=1, column=0)

        self.numero1_rectangular_real = tk.Entry(self)
        self.numero1_rectangular_real.grid(row=1, column=1)

        self.label1_rectangular = tk.Label(self, text="+")
        self.label1_rectangular.grid(row=1, column=2)

        self.numero1_rectangular_imag = tk.Entry(self)
        self.numero1_rectangular_imag.grid(row=1, column=3)

        self.label1_rectangular_i = tk.Label(self, text="i")
        self.label1_rectangular_i.grid(row=1, column=4)

        self.separador1 = tk.Label(self, text="     ")
        self.separador1.grid(row=1, column=5)

        self.numero1_polar = tk.Entry(self)
        self.numero1_polar.grid(row=1, column=6)

        self.label1_polar = tk.Label(self, text="∠")
        self.label1_polar.grid(row=1, column=7)

        self.numero1_polar_fase = tk.Entry(self)
        self.numero1_polar_fase.grid(row=1, column=8)

        self.label1_polar_grados = tk.Label(self, text="°")
        self.label1_polar_grados.grid(row=1, column=9)

        self.saveas1 = tk.Button(self, text="Guardar", command=self.guardar1)
        self.saveas1.grid(row=1, column=10)

        # Widgets número 2
        self.label2 = tk.Label(self, text="Número 2:", fg="green")
        self.label2.grid(row=2, column=0)

        self.numero2_rectangular_real = tk.Entry(self)
        self.numero2_rectangular_real.grid(row=2, column=1)

        self.label2_rectangular = tk.Label(self, text="+")
        self.label2_rectangular.grid(row=2, column=2)

        self.numero2_rectangular_imag = tk.Entry(self)
        self.numero2_rectangular_imag.grid(row=2, column=3)

        self.label2_rectangular_i = tk.Label(self, text="i")
        self.label2_rectangular_i.grid(row=2, column=4)

        self.separador2 = tk.Label(self, text="     ")
        self.separador2.grid(row=2, column=5)

        self.numero2_polar = tk.Entry(self)
        self.numero2_polar.grid(row=2, column=6)

        self.label2_polar = tk.Label(self, text="∠")
        self.label2_polar.grid(row=2, column=7)

        self.numero2_polar_fase = tk.Entry(self)
        self.numero2_polar_fase.grid(row=2, column=8)

        self.label2_polar_grados = tk.Label(self, text="°")
        self.label2_polar_grados.grid(row=2, column=9)

        self.saveas2 = tk.Button(self, text="Guardar", command=self.guardar2)
        self.saveas2.grid(row=2, column=10)

        # Botones de operaciones
        self.suma = tk.Button(self, text="+", command=self.sumar)
        self.suma.grid(row=3, column=1)

        self.resta = tk.Button(self, text="-", command=self.restar)
        self.resta.grid(row=3, column=3)

        self.multiplicacion = tk.Button(self, text="*", command=self.multiplicar)
        self.multiplicacion.grid(row=3, column=6)

        self.division = tk.Button(self, text="/", command=self.dividir)
        self.division.grid(row=3, column=8)

        #self.potencia = tk.Button(self, text="^", command=self.potencia)
        #self.potencia.grid(row=3, column=5)

        # Widgets resultado
        self.label3 = tk.Label(self, text="Resultado:", fg="red")
        self.label3.grid(row=4, column=0)

        self.resultado_rectangular_real = tk.Entry(self)
        self.resultado_rectangular_real.grid(row=4, column=1)

        self.label_rectangular = tk.Label(self, text="+")
        self.label_rectangular.grid(row=4, column=2)

        self.resultado_rectangular_imag = tk.Entry(self)
        self.resultado_rectangular_imag.grid(row=4, column=3)

        self.label_rectangular_i = tk.Label(self, text="i")
        self.label_rectangular_i.grid(row=4, column=4)

        self.separador3 = tk.Label(self, text="     ")
        self.separador3.grid(row=4, column=5)

        self.resultado_polar = tk.Entry(self)
        self.resultado_polar.grid(row=4, column=6)

        self.label_polar = tk.Label(self, text="∠")
        self.label_polar.grid(row=4, column=7)

        self.resultado_polar_fase = tk.Entry(self)
        self.resultado_polar_fase.grid(row=4, column=8)

        self.label_polar_grados = tk.Label(self, text="°")
        self.label_polar_grados.grid(row=4, column=9)

        self.saveas3 = tk.Button(self, text="Guardar", command=self.guardar3)
        self.saveas3.grid(row=4, column=10)

        # Botón 'next' que borra los campos de entrada y salida y pone la salida en el número 1, además pone focus en el número 2
        self.next_button = tk.Button(self, text="Next", command=self.next)
        self.next_button.grid(row=5, column=0)

        # Botón 'clear' que borra los campos de entrada y salida
        self.clear_button = tk.Button(self, text="Clear", command=self.clear)
        self.clear_button.grid(row=6, column=0)

        # Widgets gráfica
        self.grafica_width = 700
        self.grafica_height = 700
        self.grafica = tk.Canvas(self, width=self.grafica_width, height=self.grafica_height)
        self.grafica.grid(row=7, column=0, columnspan=12)

        # 1. Graficar los ejes
        self.grafica.delete("all")
        self.grafica.create_line(0, self.grafica_height/2, self.grafica_width, self.grafica_height/2, width=1)
        self.grafica.create_line(self.grafica_width/2, 0, self.grafica_width/2, self.grafica_height, width=1)

        # 2. Escalar el canvas a (10,0)
        self.scale_canvas(Complejo(10, 0), Complejo(0, 0), Complejo(0, 0), first=True)

    def guardar1(self):
        rec_real_1 = self.numero1_rectangular_real.get()
        rec_imag_1 = self.numero1_rectangular_imag.get()
        pol_mod_1 = self.numero1_polar.get()
        pol_fase_1 = self.numero1_polar_fase.get()

        if rec_real_1 and rec_imag_1:
            numero1 = Complejo(eval(rec_real_1,self.gl), eval(rec_imag_1,self.gl))
        elif pol_mod_1 and pol_fase_1:
            numero1 = Complejo(modulo=eval(pol_mod_1,self.gl), fase=math.radians(eval(pol_fase_1,self.gl)))
        else:
            raise ValueError("Se debe ingresar el número 1 en forma rectangular o polar")
        
        # Mostrar ventana para preguntar por el nombre de la variable
        nombre = simpledialog.askstring("Guardar", "Nombre de la variable:")
        if nombre:
            self.gl[nombre] = numero1

    def guardar2(self):
        rec_real_2 = self.numero2_rectangular_real.get()
        rec_imag_2 = self.numero2_rectangular_imag.get()
        pol_mod_2 = self.numero2_polar.get()
        pol_fase_2 = self.numero2_polar_fase.get()

        if rec_real_2 and rec_imag_2:
            numero2 = Complejo(eval(rec_real_2,self.gl), eval(rec_imag_2,self.gl))
        elif pol_mod_2 and pol_fase_2:
            numero2 = Complejo(modulo=eval(pol_mod_2,self.gl), fase=math.radians(eval(pol_fase_2,self.gl)))
        else:
            raise ValueError("Se debe ingresar el número 2 en forma rectangular o polar")

        # Mostrar ventana para preguntar por el nombre de la variable
        nombre = simpledialog.askstring("Guardar", "Nombre de la variable:")
        if nombre:
            self.gl[nombre] = numero2

    def guardar3(self):
        rec_real_3 = self.resultado_rectangular_real.get()
        rec_imag_3 = self.resultado_rectangular_imag.get()

        resultado = Complejo(eval(rec_real_3,self.gl), eval(rec_imag_3,self.gl))

        # Mostrar ventana para preguntar por el nombre de la variable
        nombre = simpledialog.askstring("Guardar", "Nombre de la variable:")
        if nombre:
            self.gl[nombre] = resultado
            
    def next(self):
        self.numero1_rectangular_real.delete(0, tk.END)
        self.numero1_rectangular_imag.delete(0, tk.END)
        self.numero1_polar.delete(0, tk.END)
        self.numero1_polar_fase.delete(0, tk.END)

        self.numero2_rectangular_real.delete(0, tk.END)
        self.numero2_rectangular_imag.delete(0, tk.END)
        self.numero2_polar.delete(0, tk.END)
        self.numero2_polar_fase.delete(0, tk.END)

        self.numero1_rectangular_real.insert(0, self.resultado_rectangular_real.get())
        self.numero1_rectangular_imag.insert(0, self.resultado_rectangular_imag.get())
        self.numero1_polar.insert(0, self.resultado_polar.get())
        self.numero1_polar_fase.insert(0, self.resultado_polar_fase.get())

        self.resultado_rectangular_real.delete(0, tk.END)
        self.resultado_rectangular_imag.delete(0, tk.END)
        self.resultado_polar.delete(0, tk.END)
        self.resultado_polar_fase.delete(0, tk.END)

        self.numero2_rectangular_real.focus_set()
    
    def clear(self):
        self.numero1_rectangular_real.delete(0, tk.END)
        self.numero1_rectangular_imag.delete(0, tk.END)
        self.numero1_polar.delete(0, tk.END)
        self.numero1_polar_fase.delete(0, tk.END)

        self.numero2_rectangular_real.delete(0, tk.END)
        self.numero2_rectangular_imag.delete(0, tk.END)
        self.numero2_polar.delete(0, tk.END)
        self.numero2_polar_fase.delete(0, tk.END)

        self.resultado_rectangular_real.delete(0, tk.END)
        self.resultado_rectangular_imag.delete(0, tk.END)
        self.resultado_polar.delete(0, tk.END)
        self.resultado_polar_fase.delete(0, tk.END)

        self.numero1_rectangular_real.focus_set()

    def scale_canvas(self, number1, number2, result, first=False):
        # 0. Graficar los ejes
        self.grafica.delete("all")
        self.grafica.create_line(0, self.grafica_height/2, self.grafica_width, self.grafica_height/2, width=1)
        self.grafica.create_line(self.grafica_width/2, 0, self.grafica_width/2, self.grafica_height, width=1)

        # 1. Hallar el módulo del número más grande
        max_module = max(number1.modulo, number2.modulo, result.modulo)
        print(max_module)
        
        # 2. La escala será el tamaño del canvas entre el módulo más grande
        scale = self.grafica_width/(2*max_module)
        print(scale)

        # 3. El tamaño del circulo unitario será 1 unidad de escala
        unit_circle_radius = scale
        self.grafica.create_oval(self.grafica_width/2 - unit_circle_radius, self.grafica_height/2 - unit_circle_radius, self.grafica_width/2 + unit_circle_radius, self.grafica_height/2 + unit_circle_radius, width=1)

        # 4. Numerar los ejes desde 0 hasta lo que se pueda
        num_nums = 10
        i = 1
        for i in range(1, num_nums+1):
            i = (((max_module/num_nums)*i)*1000//1)/1000
            if max_module >= num_nums:
                i = int(i)
            self.grafica.create_text(self.grafica_width/2 + i*unit_circle_radius, self.grafica_height/2 + 5, text=str(i), font=("Arial", 5))
            self.grafica.create_text(self.grafica_width/2 - i*unit_circle_radius, self.grafica_height/2 + 5, text=str(-i), font=("Arial", 5))
            self.grafica.create_text(self.grafica_width/2 + 5, self.grafica_height/2 - i*unit_circle_radius, text=str(i), font=("Arial", 5))
            self.grafica.create_text(self.grafica_width/2 + 5, self.grafica_height/2 + i*unit_circle_radius, text=str(-i), font=("Arial", 5))
        
        # 5. Graficar los números
        if not first:
            self.grafica.create_line(self.grafica_width/2, self.grafica_height/2, self.grafica_width/2 + number1.real*scale, self.grafica_height/2 - number1.imag*scale, width=2, fill="blue")
            self.grafica.create_line(self.grafica_width/2, self.grafica_height/2, self.grafica_width/2 + number2.real*scale, self.grafica_height/2 - number2.imag*scale, width=2, fill="green")
            self.grafica.create_line(self.grafica_width/2, self.grafica_height/2, self.grafica_width/2 + result.real*scale, self.grafica_height/2 - result.imag*scale, width=2, fill="red")

    def obtener_numeros(self):
        rec_real_1 = self.numero1_rectangular_real.get()
        rec_imag_1 = self.numero1_rectangular_imag.get()
        pol_mod_1 = self.numero1_polar.get()
        pol_fase_1 = self.numero1_polar_fase.get()

        if rec_real_1 and rec_imag_1:
            numero1 = Complejo(eval(rec_real_1,self.gl), eval(rec_imag_1,self.gl))
        elif pol_mod_1 and pol_fase_1:
            numero1 = Complejo(modulo=eval(pol_mod_1,self.gl), fase=math.radians(eval(pol_fase_1,self.gl)))
        else:
            raise ValueError("Se debe ingresar el número 1 en forma rectangular o polar")
        
        rec_real_2 = self.numero2_rectangular_real.get()
        rec_imag_2 = self.numero2_rectangular_imag.get()
        pol_mod_2 = self.numero2_polar.get()
        pol_fase_2 = self.numero2_polar_fase.get()

        if rec_real_2 and rec_imag_2:
            numero2 = Complejo(eval(rec_real_2,self.gl), eval(rec_imag_2,self.gl))
        elif pol_mod_2 and pol_fase_2:
            numero2 = Complejo(modulo=eval(pol_mod_2,self.gl), fase=math.radians(eval(pol_fase_2,self.gl)))
        else:
            raise ValueError("Se debe ingresar el número 2 en forma rectangular o polar")
        
        return numero1, numero2

    def sumar(self):
        numero1, numero2 = self.obtener_numeros()
        resultado = numero1.sumar(numero2)
        self.mostrar_resultado(resultado)

    def restar(self):
        numero1, numero2 = self.obtener_numeros()
        resultado = numero1.restar(numero2)
        self.mostrar_resultado(resultado)

    def multiplicar(self):
        numero1, numero2 = self.obtener_numeros()
        resultado = numero1.multiplicar(numero2)
        self.mostrar_resultado(resultado)

    def dividir(self):
        numero1, numero2 = self.obtener_numeros()
        resultado = numero1.dividir(numero2)
        self.mostrar_resultado(resultado)

    #def potencia(self):
    #    numero1, numero2 = self.obtener_numeros()
    #    resultado = numero1.potencia(numero2)
    #    self.mostrar_resultado(resultado)

    def mostrar_resultado(self, resultado):
        numero1, numero2 = self.obtener_numeros()

        # Completar los campos de los números digitados
        self.numero1_rectangular_real.delete(0, tk.END)
        self.numero1_rectangular_imag.delete(0, tk.END)
        self.numero1_rectangular_real.insert(0, f"{numero1.real}")
        self.numero1_rectangular_imag.insert(0, f"{numero1.imag}")

        self.numero1_polar.delete(0, tk.END)
        self.numero1_polar_fase.delete(0, tk.END)
        self.numero1_polar.insert(0, f"{numero1.modulo}")
        deg = math.degrees(numero1.fase)
        self.numero1_polar_fase.insert(0, f"{deg}")

        self.numero2_rectangular_real.delete(0, tk.END)
        self.numero2_rectangular_imag.delete(0, tk.END)
        self.numero2_rectangular_real.insert(0, f"{numero2.real}")
        self.numero2_rectangular_imag.insert(0, f"{numero2.imag}")

        self.numero2_polar.delete(0, tk.END)
        self.numero2_polar_fase.delete(0, tk.END)
        self.numero2_polar.insert(0, f"{numero2.modulo}")
        deg = math.degrees(numero2.fase)
        self.numero2_polar_fase.insert(0, f"{deg}")

        # Completar los campos de resultado
        self.resultado_rectangular_real.delete(0, tk.END)
        self.resultado_rectangular_imag.delete(0, tk.END)
        self.resultado_rectangular_real.insert(0, f"{resultado.real}")
        self.resultado_rectangular_imag.insert(0, f"{resultado.imag}")

        self.resultado_polar.delete(0, tk.END)
        self.resultado_polar_fase.delete(0, tk.END)
        self.resultado_polar.insert(0, f"{resultado.modulo if abs(resultado.modulo) > min_acceptable else 0}")
        deg = math.degrees(resultado.fase)
        self.resultado_polar_fase.insert(0, f"{deg if abs(deg) > min_acceptable else 0}")

        # Graficar
        self.scale_canvas(numero1, numero2, resultado)

def main(*args, **kwargs):
    a = Complejo(1, 1)
    print(a)
    b = Complejo(modulo=1, fase=math.pi/8+2*math.pi)
    print(b)
    c = a.multiplicar(b)
    print(c)
    print(c.polar())
    root = tk.Tk()
    app = CalculadoraComplejos(master=root)
    app.mainloop()

if __name__ == "__main__" :
    main()
