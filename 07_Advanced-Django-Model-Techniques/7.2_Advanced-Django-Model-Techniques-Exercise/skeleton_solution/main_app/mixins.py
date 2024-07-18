class RechargeEnergyMixin:
    def recharge_energy(self, amount: int) -> None:
        self.energy = min(self.energy + amount, 100)
        self.save()