import uuid

def generate_tracking_code():
    tracking_code = f"PKG-{uuid.uuid4().hex[:12].upper()}"
    return tracking_code



def calculate_freight(weight_kg: float, volume_cm3: float):
   frete = (weight_kg * 2.5) + (volume_cm3 * 0.001)
   return frete
