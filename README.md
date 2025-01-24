# Tildagon clock

| Button | |
|---|---|
| UP (A) | choose a different marker shape |
| RIGHT (B) | change the colour-rotation direction |
| CONFIRM (C) | toggle filled markers |
| DOWN (D) | rotating spectrum or single (changing) colour |
| LEFT (E) | rotate the clock (so you can stand the badge on a different side). The 12:00 position is briefly highlighted |
| CANCEL (F) | minimise app |

## Install locally (not via app store)

You need [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html), then:

```bash
make mkdir
make push connect
```

Wait while it pushes the code to the badge, then `ctrl-d`, the badge will reboot and you should see a new app called `Clock`
