from typing import List

class Faktura:
    def __init__(self):
        self.TypSprzedazy: str = ""
        self.ZaplaconoNaDokumencie: float = 0.0
        self.Zaplacono: float = 0.0
        self.LiczOd: str = ""
        self.NumerKontaBankowego: str = ""
        self.DataWystawienia: str = ""
        self.MiejsceWystawienia: str = ""
        self.DataSprzedazy: str = ""
        self.FormatDatySprzedazy: str = ""
        self.SposobZaplaty: str = ""
        self.Jezyk: str = ""
        self.Waluta: str = ""
        self.KursWalutyWidoczny: bool = False
        self.KursWalutyZDniaPoprzedzajacegoDzienWystawieniaFaktury: float = None
        self.RodzajPodpisuOdbiorcy: str = ""
        self.WidocznyNumerGios: bool = False
        self.WidocznyNumerBdo: bool = False
        self.Numer: int = None
        self.Pozycje: List[PozycjaFaktury] = []
        self.Kontrahent: Kontrahent = None

class PozycjaFaktury:
    def __init__(self):
        self.StawkaVat: float = 0.0
        self.Ilosc: float = 0.0
        self.CenaJednostkowa: float = 0.0
        self.NazwaPelna: str = ""
        self.Jednostka: str = ""
        self.TypStawkiVat: str = ""

class Kontrahent:
    def __init__(self):
        self.Nazwa: str = ""
        self.NIP: str = ""
        self.Ulica: str = ""
        self.KodPocztowy: str = ""
        self.Kraj: str = ""
        self.Miejscowosc: str = ""