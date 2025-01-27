# Tildagon clock

| Button | |
|---|---|
| UP (A) | choose a different marker shape |
| CONFIRM (C) | toggle filled markers |
| RIGHT (B) | make the markers bigger |
| LEFT (E) | make the markers smaller |
| DOWN (D) | rotating spectrum or single (changing) colour |
| CANCEL (F) | minimise app |

## Install it

It's on the [app store](https://apps.badge.emfcamp.org/) as "Sam's Clock". Or,

## Install from your laptop

You need [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html), then:

```bash
make mkdir
make push connect
```

Wait while it pushes the code to the badge, then `ctrl-d`, the badge will reboot and you should see a new app called `Clock`.

> Note: the badge *must* be connected to some sort of Wifi when the app starts-up so it can do `ntptime.settime()`. Without this it crashes hard.
