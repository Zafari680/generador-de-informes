import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Analysis and Report Generator")
        self.setGeometry(100, 100, 600, 400)

        # Configuración del layout principal
        self.layout = QVBoxLayout()

        # Etiqueta de muestra
        self.label = QLabel("Bienvenido a la aplicación de análisis de datos", self)
        self.layout.addWidget(self.label)

        # Botón para cargar datos
        self.load_data_button = QPushButton("Cargar Datos", self)
        self.load_data_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_data_button)

        # Botón para generar informe
        self.generate_report_button = QPushButton("Generar Informe", self)
        self.generate_report_button.clicked.connect(self.generate_report)
        self.layout.addWidget(self.generate_report_button)

        # Configurar el widget central
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Inicializar variable de datos
        self.data = None

    def load_data(self):
        """Función para cargar datos desde un archivo XLSX y filtrar columnas numéricas."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar archivo XLSX", "", "Archivos XLSX (*.xlsx)", options=options)
        if file_name:
            self.data = pd.read_excel(file_name, engine='openpyxl')

            # Filtrar solo columnas numéricas
            self.data = self.data.select_dtypes(include=['number'])
            
            if self.data.empty:
                self.label.setText("El archivo no contiene datos numéricos.")
            else:
                self.label.setText(f"Datos cargados: {file_name}")

    def generate_report(self):
        """Función para analizar datos y generar un informe."""
        if self.data is not None and not self.data.empty:
            try:
                # Verificar que hay suficientes columnas para el análisis
                if self.data.shape[1] < 2:
                    self.label.setText("El archivo debe contener al menos dos columnas numéricas.")
                    return

                # Realizar un análisis simple (Regresión Lineal)
                X = self.data.iloc[:, :-1].values
                y = self.data.iloc[:, -1].values

                model = LinearRegression()
                model.fit(X, y)

                # Predicciones
                predictions = model.predict(X)

                # Graficar los resultados
                plt.scatter(X, y, color='red')
                plt.plot(X, predictions, color='blue')
                plt.title('Análisis de datos')
                plt.xlabel('Variable independiente')
                plt.ylabel('Variable dependiente')
                plt.savefig('analisis_resultado.png')

                # Generar informe PDF
                self.create_pdf_report(predictions)

                self.label.setText("Informe generado exitosamente.")
            except Exception as e:
                self.label.setText(f"Error en el análisis de datos: {e}")
        else:
            self.label.setText("Por favor, cargue datos válidos primero.")

    def create_pdf_report(self, predictions):
        """Función para crear un informe PDF."""
        c = canvas.Canvas("Informe_analisis_datos.pdf")
        c.drawString(100, 750, "Informe de Análisis de Datos")
        c.drawImage("analisis_resultado.png", 50, 450, width=500, height=250)
        c.drawString(100, 400, "Predicciones:")

        for i, prediction in enumerate(predictions[:10], start=1):  # Limitar las predicciones en el informe
            c.drawString(100, 400 - i*20, f"Predicción {i}: {prediction:.2f}")

        c.save()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec_())
