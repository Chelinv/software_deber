def calcular_promedio(calificaciones: list[float]) -> float:
    """
    Calcula el promedio de una lista de calificaciones.
    
    Args:
        calificaciones (list[float]): Lista de notas.
        
    Returns:
        float: El promedio de las notas.
        
    Examples:
        >>> calcular_promedio([10, 8, 9])
        9.0
        >>> calcular_promedio([5.5, 6.5, 7.5])
        6.5
        >>> calcular_promedio([])
        0.0
    """
    if not calificaciones:
        return 0.0
    return sum(calificaciones) / len(calificaciones)

def es_aprobado(promedio: float, nota_minima: float = 7.0) -> bool:
    """
    Determina si un promedio es aprobatorio.
    
    Args:
        promedio (float): El promedio del estudiante.
        nota_minima (float): La nota mínima para aprobar.
        
    Returns:
        bool: True si aprobó, False en caso contrario.
        
    Examples:
        >>> es_aprobado(8.0)
        True
        >>> es_aprobado(6.9)
        False
        >>> es_aprobado(7.0)
        True
    """
    return promedio >= nota_minima
