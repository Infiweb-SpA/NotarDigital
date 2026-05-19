from app.extensions import db
from app.models import User, OfficeConfig, ServiceCategory, Service

def seed_data():
    """
    Crea o actualiza datos iniciales:
    - Usuario administrador
    - Configuración de la notaría
    - Categorías de servicios
    - Servicios con tarifas en CLP
    """
    # 1. Administrador
    if not User.query.filter_by(email="admin@notaria.cl").first():
        user = User(
            nombre="Administrador",
            rut="11111111-1",
            email="admin@notaria.cl",
            rol="admin",
            cargo="Administrador"
        )
        user.set_password("123456")
        db.session.add(user)
        print("✅ Usuario admin@notaria.cl creado.")

    # 2. Configuración de oficina
    if not OfficeConfig.query.first():
        office = OfficeConfig(
            nombre_notaria="Notaría Demo Araucanía",
            direccion="Calle Principal 123",
            comuna="Temuco",
            region="La Araucanía",
            correo_oficial="contacto@notaria.cl",
            telefono="+56 9 1234 5678",
            horario_apertura="09:00",
            horario_cierre="17:00",
            horas_minimas_atencion=7
        )
        db.session.add(office)
        print("✅ Configuración de oficina inicial creada.")

    # 3. Categorías de servicios (ordenadas)
    categorias_data = [
        {"nombre": "Certificados", "descripcion": "Emisión de certificados notariales", "orden": 1},
        {"nombre": "Firmas y Legalizaciones", "descripcion": "Legalización de firmas y documentos", "orden": 2},
        {"nombre": "Trámites de Bienes Raíces", "descripcion": "Compraventa, hipotecas, arriendos", "orden": 3},
        {"nombre": "Constitución de Sociedades", "descripcion": "Creación y modificación de empresas", "orden": 4},
        {"nombre": "Poderes", "descripcion": "Otorgamiento de poderes generales o especiales", "orden": 5},
        {"nombre": "Testamentos", "descripcion": "Testamentos abiertos y cerrados", "orden": 6},
        {"nombre": "Trámites Varios", "descripcion": "Otros servicios notariales", "orden": 7},
    ]

    categorias_creadas = {}
    for cat_data in categorias_data:
        categoria = ServiceCategory.query.filter_by(nombre=cat_data["nombre"]).first()
        if not categoria:
            categoria = ServiceCategory(
                nombre=cat_data["nombre"],
                descripcion=cat_data["descripcion"],
                activo=True,
                orden=cat_data["orden"]
            )
            db.session.add(categoria)
            print(f"✅ Categoría '{cat_data['nombre']}' creada.")
        else:
            # Actualizar por si cambian descripción u orden
            categoria.descripcion = cat_data["descripcion"]
            categoria.orden = cat_data["orden"]
            print(f"🔄 Categoría '{cat_data['nombre']}' ya existe, se actualizó.")
        categorias_creadas[cat_data["nombre"]] = categoria

    db.session.flush()  # Para obtener los IDs sin commit completo

    # 4. Servicios con tarifas en CLP (pesos chilenos)
    servicios_data = [
        # Certificados
        {"categoria": "Certificados", "nombre": "Certificado de Firma", "descripcion": "Certificación de firma en documento", "tarifa": 2500},
        {"categoria": "Certificados", "nombre": "Certificado de Existencia", "descripcion": "Certificado de existencia legal", "tarifa": 3500},
        {"categoria": "Certificados", "nombre": "Certificado de Matrimonio", "descripcion": "Certificado notarial de matrimonio", "tarifa": 4000},
        
        # Firmas y Legalizaciones
        {"categoria": "Firmas y Legalizaciones", "nombre": "Legalización de Firma", "descripcion": "Legalización de firma en documento simple", "tarifa": 2000},
        {"categoria": "Firmas y Legalizaciones", "nombre": "Legalización de Documento Extranjero", "descripcion": "Apostilla o legalización consular", "tarifa": 12000},
        
        # Bienes Raíces
        {"categoria": "Trámites de Bienes Raíces", "nombre": "Escritura de Compraventa", "descripcion": "Minuta y otorgamiento de compraventa", "tarifa": 50000},
        {"categoria": "Trámites de Bienes Raíces", "nombre": "Constitución de Hipoteca", "descripcion": "Escritura de hipoteca", "tarifa": 35000},
        {"categoria": "Trámites de Bienes Raíces", "nombre": "Contrato de Arriendo", "descripcion": "Otorgamiento de contrato de arrendamiento", "tarifa": 25000},
        
        # Sociedades
        {"categoria": "Constitución de Sociedades", "nombre": "Constitución de EIRL", "descripcion": "Empresa Individual de Responsabilidad Limitada", "tarifa": 80000},
        {"categoria": "Constitución de Sociedades", "nombre": "Constitución de SpA", "descripcion": "Sociedad por Acciones", "tarifa": 90000},
        {"categoria": "Constitución de Sociedades", "nombre": "Modificación de Sociedad", "descripcion": "Reforma de estatutos", "tarifa": 45000},
        
        # Poderes
        {"categoria": "Poderes", "nombre": "Poder General", "descripcion": "Poder general para representación", "tarifa": 15000},
        {"categoria": "Poderes", "nombre": "Poder Especial", "descripcion": "Poder para acto específico", "tarifa": 10000},
        {"categoria": "Poderes", "nombre": "Revocación de Poder", "descripcion": "Revocación de poder otorgado", "tarifa": 8000},
        
        # Testamentos
        {"categoria": "Testamentos", "nombre": "Testamento Abierto", "descripcion": "Testamento otorgado ante notario", "tarifa": 30000},
        {"categoria": "Testamentos", "nombre": "Testamento Cerrado", "descripcion": "Testamento en sobre cerrado", "tarifa": 25000},
        
        # Varios
        {"categoria": "Trámites Varios", "nombre": "Certificado de Viaje (Menor)", "descripcion": "Autorización para salida de menores", "tarifa": 8000},
        {"categoria": "Trámites Varios", "nombre": "Declaración Jurada", "descripcion": "Declaración jurada simple", "tarifa": 3000},
    ]

    for serv_data in servicios_data:
        categoria = categorias_creadas.get(serv_data["categoria"])
        if not categoria:
            print(f"⚠️ Categoría '{serv_data['categoria']}' no encontrada, se omite servicio '{serv_data['nombre']}'")
            continue
        
        servicio = Service.query.filter_by(nombre=serv_data["nombre"], category_id=categoria.id).first()
        if not servicio:
            servicio = Service(
                nombre=serv_data["nombre"],
                descripcion=serv_data["descripcion"],
                tarifa=serv_data["tarifa"],
                activo=True,
                category_id=categoria.id
            )
            db.session.add(servicio)
            print(f"✅ Servicio '{serv_data['nombre']}' (${serv_data['tarifa']:,} CLP) creado.")
        else:
            # Actualizar descripción y tarifa por si cambian
            servicio.descripcion = serv_data["descripcion"]
            servicio.tarifa = serv_data["tarifa"]
            print(f"🔄 Servicio '{serv_data['nombre']}' ya existe, se actualizó tarifa a ${serv_data['tarifa']:,} CLP.")

    db.session.commit()
    print("🚀 Proceso de seed finalizado con éxito (categorías y servicios incluidos).")