from flask import Blueprint

from app.modules.dashboard.model import VentasPorMes,MermasPorMes,ProductoMasProducido,ProductoMasVendido

__all__ = ["VentasPorMes","MermasPorMes","ProductoMasVendido","ProductoMasProducido"]
