# main.py

"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Software FJ
"""

from excepciones import (
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    DatosIncorrectosError,
    OperacionNoPermitidaError
)
from utilidades import logger
from clases import Cliente, ServicioSala, ServicioEquipo, ServicioAsesoria, Reserva


def pruebas_sistema_completo():
    """Pruebas completas del sistema con al menos 10 operaciones"""
    
    print("=" * 70)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 70)
    
    # Variables para almacenar objetos creados
    clientes_validos = []
    servicios_validos = []
    reservas = []
    
    # ========== OPERACIÓN 1-3: CREAR CLIENTES ==========
    print("\n" + "=" * 70)
    print("OPERACIONES 1-3: CREACIÓN DE CLIENTES")
    print("=" * 70)
    
    # Operación 1: Cliente válido
    try:
        print("\n[1] Creando cliente válido: carlos peña...")
        cliente1 = Cliente(
            nombre="carlos peña",
            email="c.pena@email.com",
            telefono="3126618729",
            documento="5736024320"
        )
        clientes_validos.append(cliente1)
        print(f"✓ ÉXITO: {cliente1}")
    except ClienteInvalidoError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 2: Cliente sin teléfono (válido con warning)
    try:
        print("\n[2] Creando cliente sin teléfono: María González...")
        cliente2 = Cliente(
            nombre="María González",
            email="maria.g@email.com"
        )
        clientes_validos.append(cliente2)
        print(f"✓ ÉXITO: {cliente2}")
    except ClienteInvalidoError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 3: Cliente inválido (email incorrecto) - DEBE FALLAR
    try:
        print("\n[3] Intentando crear cliente con email inválido...")
        cliente3 = Cliente(
            nombre="Pedro López",
            email="email-sin-formato",
            telefono="3009876543"
        )
        print(f"✓ Cliente creado: {cliente3}")
    except (ClienteInvalidoError, DatosIncorrectosError) as e:
        print(f"✗ ERROR ESPERADO: {e.mensaje}")
        print("   → Sistema manejó correctamente el error ✓")
    
    # ========== OPERACIÓN 4-6: CREAR SERVICIOS ==========
    print("\n" + "=" * 70)
    print("OPERACIONES 4-6: CREACIÓN DE SERVICIOS")
    print("=" * 70)
    
    # Operación 4: Servicio Sala
    try:
        print("\n[4] Creando servicio de sala...")
        sala = ServicioSala(
            nombre="Sala de Reuniones Premium",
            descripcion="Sala equipada con tecnología avanzada",
            precio_base=50000,
            capacidad=20,
            equipamiento="Proyector 4K, TV 65', Pizarra digital"
        )
        servicios_validos.append(sala)
        print(f"✓ ÉXITO: {sala}")
        print(f"   Costo 3 horas: ${sala.calcular_costo(horas=3)}")
    except ServicioNoDisponibleError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 5: Servicio Equipo
    try:
        print("\n[5] Creando servicio de equipo...")
        equipo = ServicioEquipo(
            nombre="Laptop HP EliteBook",
            descripcion="Laptop empresarial de alto rendimiento",
            precio_base=30000,
            tipo_equipo="Laptop",
            cantidad_disponible=5
        )
        servicios_validos.append(equipo)
        print(f"✓ ÉXITO: {equipo}")
        print(f"   Costo 2 días: ${equipo.calcular_costo(dias=2)}")
    except ServicioNoDisponibleError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 6: Servicio Asesoría
    try:
        print("\n[6] Creando servicio de asesoría...")
        asesoria = ServicioAsesoria(
            nombre="Asesoría en Desarrollo de Software",
            descripcion="Consultoría especializada en arquitectura",
            precio_base=80000,
            especialidad="Desarrollo de Software",
            duracion_sesion=90
        )
        servicios_validos.append(asesoria)
        print(f"✓ ÉXITO: {asesoria}")
        print(f"   Costo 1 sesión: ${asesoria.calcular_costo(sesiones=1)}")
    except ServicioNoDisponibleError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # ========== OPERACIÓN 7-10: CREAR Y GESTIONAR RESERVAS ==========
    print("\n" + "=" * 70)
    print("OPERACIONES 7-10: CREACIÓN Y GESTIÓN DE RESERVAS")
    print("=" * 70)
    
    # Operación 7: Crear reserva válida
    try:
        print("\n[7] Creando reserva de sala para carlos peña...")
        reserva1 = Reserva(
            cliente=cliente1,
            servicio=sala,
            parametros_servicio={'horas': 4, 'descuento': 10}
        )
        reservas.append(reserva1)
        print(f"✓ ÉXITO: {reserva1}")
        print(f"   Resumen: {reserva1.obtener_resumen()}")
    except ReservaInvalidaError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 8: Confirmar reserva
    try:
        print("\n[8] Confirmando reserva de sala...")
        reserva1.confirmar()
        print(f"✓ ÉXITO: Reserva confirmada - Estado: {reserva1.estado}")
    except OperacionNoPermitidaError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 9: Crear y procesar reserva completa
    try:
        print("\n[9] Creando y procesando reserva de equipo para María...")
        reserva2 = Reserva(
            cliente=cliente2,
            servicio=equipo,
            parametros_servicio={'dias': 3, 'cantidad': 2, 'seguro': True}
        )
        reservas.append(reserva2)
        print(f"✓ Reserva creada: {reserva2}")
        
        # Procesar (confirmar + completar)
        print("   Procesando reserva...")
        if reserva2.procesar():
            print(f"✓ ÉXITO: Reserva procesada - Estado: {reserva2.estado}")
        else:
            print("✗ ERROR: No se pudo procesar")
            
    except ReservaInvalidaError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 10: Intentar operación no permitida - DEBE FALLAR
    try:
        print("\n[10] Intentando confirmar una reserva ya completada...")
        reserva2.confirmar()  # Ya está COMPLETADA, debe fallar
        print("✓ Reserva confirmada")
    except OperacionNoPermitidaError as e:
        print(f"✗ ERROR ESPERADO: {e.mensaje}")
        print("   → Sistema manejó correctamente el error ✓")
    
    # ========== OPERACIONES ADICIONALES ==========
    print("\n" + "=" * 70)
    print("OPERACIONES ADICIONALES: CASOS AVANZADOS")
    print("=" * 70)
    
    # Operación 11: Crear reserva de asesoría
    try:
        print("\n[11] Creando reserva de asesoría grupal...")
        reserva3 = Reserva(
            cliente=cliente1,
            servicio=asesoria,
            parametros_servicio={'sesiones': 3, 'grupal': True}
        )
        reservas.append(reserva3)
        print(f"✓ ÉXITO: {reserva3}")
        print(f"   Costo total: ${reserva3.costo_total}")
    except ReservaInvalidaError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 12: Recalcular costo
    try:
        print("\n[12] Recalculando costo de la reserva de asesoría...")
        costo_anterior = reserva3.costo_total
        reserva3.recalcular_costo({'sesiones': 5, 'grupal': False})
        print(f"✓ ÉXITO: Costo recalculado")
        print(f"   Anterior: ${costo_anterior} → Nuevo: ${reserva3.costo_total}")
    except OperacionNoPermitidaError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 13: Cancelar reserva
    try:
        print("\n[13] Cancelando reserva de asesoría...")
        reserva3.cancelar(motivo="Cliente canceló por conflicto de horario")
        print(f"✓ ÉXITO: Reserva cancelada - Estado: {reserva3.estado}")
    except OperacionNoPermitidaError as e:
        print(f"✗ ERROR: {e.mensaje}")
    
    # Operación 14: Intentar completar reserva cancelada - DEBE FALLAR
    try:
        print("\n[14] Intentando completar una reserva cancelada...")
        reserva3.completar()
        print("✓ Reserva completada")
    except OperacionNoPermitidaError as e:
        print(f"✗ ERROR ESPERADO: {e.mensaje}")
        print("   → Sistema manejó correctamente el error ✓")
    
    # Operación 15: Crear servicio con precio inválido - DEBE FALLAR
    try:
        print("\n[15] Intentando crear servicio con precio negativo...")
        servicio_invalido = ServicioSala(
            nombre="Sala Test",
            descripcion="Prueba",
            precio_base=-1000,
            capacidad=10
        )
        print(f"✓ Servicio creado: {servicio_invalido}")
    except (ServicioNoDisponibleError, DatosIncorrectosError) as e:
        print(f"✗ ERROR ESPERADO: {e.mensaje}")
        print("   → Sistema manejó correctamente el error ✓")
    
    # ========== DEMOSTRACIÓN DE POLIMORFISMO ==========
    print("\n" + "=" * 70)
    print("DEMOSTRACIÓN: POLIMORFISMO EN ACCIÓN")
    print("=" * 70)
    print("\nTodos los servicios usan calcular_costo() pero con diferente lógica:\n")
    
    for servicio in servicios_validos:
        print(f"• {servicio.nombre}:")
        if isinstance(servicio, ServicioSala):
            print(f"  → Por horas: ${servicio.calcular_costo(horas=2)}")
        elif isinstance(servicio, ServicioEquipo):
            print(f"  → Por días: ${servicio.calcular_costo(dias=4)}")
        elif isinstance(servicio, ServicioAsesoria):
            print(f"  → Por sesiones: ${servicio.calcular_costo(sesiones=2)}")
    
    # ========== RESUMEN FINAL ==========
    print("\n" + "=" * 70)
    print("RESUMEN DEL SISTEMA")
    print("=" * 70)
    print(f"\n📊 Estadísticas:")
    print(f"   • Clientes registrados: {len(clientes_validos)}")
    print(f"   • Servicios disponibles: {len(servicios_validos)}")
    print(f"   • Reservas creadas: {len(reservas)}")
    
    print(f"\n📋 Estado de Reservas:")
    for reserva in reservas:
        print(f"   • {reserva}")
    
    print("\n" + "=" * 70)
    print("✓ PRUEBAS COMPLETADAS - Sistema funcionando correctamente")
    print("📄 Revisa 'eventos.log' para el registro completo de eventos")
    print("=" * 70)


if __name__ == "__main__":
    """Punto de entrada del programa"""
    try:
        pruebas_sistema_completo()
    except Exception as e:
        logger.critical(f"Error crítico en el sistema: {e}")
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()