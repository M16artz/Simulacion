def probabilidad_infeccion(beta: float, infectados: int, poblacion: int) -> float:
    """Probabilidad de infección individual durante un paso discreto."""
    return 1 - (1 - beta / poblacion) ** infectados
