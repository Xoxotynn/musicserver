# Нишевый мьюзик соса бэйби сервер (Navidrome + SoundCloud) 

Docker-контейнеры:
1. **Navidrome** - стриминговый сервер
2. **Sync-Worker** - среда с утилитами и скриптами для регулярной синхронизации библиотеки с ск

---

## Требования к хосту

* если сервер разворачивается на Windows, то нужно установить и подготовить WSL2 (Debian)

---

## Подготовка окружения Windows (WSL2)

> Этот шаг нужен **только** если хост на Windows. При развертывании на Linux сервере можно скипнуть.

### 1. Конфигурация ресурсов и сети
Чтобы не жрало ресурсы нужно задать лимиты
Создай файл `.wslconfig` в (`C:\Users\USERNAME\.wslconfig`):

```ini
[wsl2]
memory=8GB
processors=6
swap=2GB
autoMemoryReclaim=dropcache
networkingMode=mirrored
localhostForwarding=true
```
Режим `networkingMode=mirrored` важен, если на пк поднят VPN, и необходимо пробрасывать эти настройки внутрь WSL для корректного исходящего подключения

### 2. Проброс портов
Для доступа к серверу из локальной сети пробрось порт из Windows в WSL2

Запусти PowerShell от админа и выполни:
```powershell
netsh interface portproxy add v4tov4 listenport=4533 listenaddress=0.0.0.0 connectport=4533 connectaddress=127.0.0.1
```

### 3. Настройка Брандмауэра Windows
Разрешаем входящие подключения для порта 4533 
Зайди в **Windows Defender Firewall with Advanced Security** -> **Inbound Rules** -> **Add rule** 
Параметры:
* **Rule type:** Port
* **Protocol:** TCP
* **Specific rule ports:** 4533
* **Action:** Allow the connection
* **Profiles:** All (Domain, Private, Public)
* **Name:** navidrome

---

## Установка и развертывание

```bash
bash <(curl -s https://gist.githubusercontent.com/Xoxotynn/fbaa8805300f8384449b45c3dd8a5b34/raw/d88576da7aba758810f8a8d0b8244ec39d5fba84/bootstrap.sh)
```

или

```bash
wget -qO- https://gist.githubusercontent.com/Xoxotynn/fbaa8805300f8384449b45c3dd8a5b34/raw/d88576da7aba758810f8a8d0b8244ec39d5fba84/bootstrap.sh | bash
```


**После установки:**
```bash
cp .env.example .env
nano .env   # Заполни свои данные
./setup.sh
```

---

## Настройка доступа из интернета

Для доступа также нужно пробросить порт 4533 на роутере

Если роутер на OpenWRT, проброс можно настроить через LuCI (раздел *Network -> Firewall -> Port Forwards*) или по SSH:

```bash
uci add firewall redirect
uci set firewall.@redirect[-1].name='Navidrome_WAN'
uci set firewall.@redirect[-1].src='wan'
uci set firewall.@redirect[-1].src_dport='4533'
uci set firewall.@redirect[-1].dest='lan'
uci set firewall.@redirect[-1].dest_ip='SERVER_LOCAL_IP'
uci set firewall.@redirect[-1].dest_port='4533'
uci set firewall.@redirect[-1].target='DNAT'
uci commit firewall
/etc/init.d/firewall restart
```

---

## Использование и управление

Интерфейс Navidrome будет доступен по адресу: `http://<ВНЕШНИЙ_IP>:4533`

Синхронизация происходит каждые 7 дней.
Если нужно **принудительно запустить синхронизацию вручную**:

```bash
docker compose exec sync-worker /app/scripts/full_sync.sh
```