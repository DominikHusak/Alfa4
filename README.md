# Alfa4

Tento skript v Pythonu implementuje službu UDP pro komunikaci mezi uzly. Umoužňuje uzlům v síti se navzájem objevit a vyměňovat si zprávy.

## Funkce

- **UDPListener - posluchač**: Naslouchá na zadaném portu pro UDP zprávy a zpracovává příchozí zprávy.
- **UDPBroadcaster - vysílač**: Pravidelně vysílá "hello" zprávy všem uzlům v síti.
- **UDPDiscovery - objevování**: Objevuje uzly v síti a udržuje seznam aktivních uzlů.
- **Zpracování odpovědí**: Odpovídá na "hello" zprávy od jiných uzlů, aby potvrdil jejich přítomnost.

## Požadavky

- Python verze 3.X
- Knihovna `socket`
- Knihovna `json`
- Knihovna `threading`

## Použití

1. Ujistěte se, že je Python verze 3.0 a vyšší nainstalována.
2. Upravte konfigurační parametry v `conf.py` podle nastavení vaší sítě.
3. Spusťte skript `main.py`.

```
python main.py
```

## Konfigurace
- V conf.py můžete konfigurovat následující parametry:

1. BROADCAST_IP: IP adresa použitá pro UDP vysílání.
2. UDP_PORT: Číslo portu pro UDP komunikaci.
3. PEER_ID: Unikátní ID uzlů.

## Třídy

### UDPListener

- __init__(self, sock, callback): Inicializuje UDP posluchač se sockety a funkcemi zpětného volání.
- run(self): Poslouchá přicházející UDP zprávy.
- stop(self): Zastavuje UDP posluchač.

### UDPBroadcaster

- __init__(self, sock): Inicializuje UDP vysílač se socketem.
- run(self): Vysílá "hello" zprávy všem uzlům.
- stop(self): Zastavuje UDP vysílač.

### UDPDiscovery

- __init__(self): Inicializuje službu UDP objevování.
- handle_hello_message(self, message, addr): Zpracovává příchozí "hello" zprávy od uzlů.
- handle_response_message(self, message, addr): Zpracovává příchozí odpovědi od uzlů.
- send_response(self, addr): Odesílá zpětnou odpověď uzlu.
- start_discovery(self): Spouští proces UDP objevování.