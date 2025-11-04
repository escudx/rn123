# PARTE 1/6 — Base & i18n (Português/Espanhol)
# - Imports básicos, captura global de erros (popup)
# - Setup do CustomTkinter
# - Constantes do app (sem UI ainda)
# - Dicionário de idioma + helpers de texto
# - Funções de montagem textual reutilizadas nas próximas partes

import sys, traceback, os, json
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk


class SafeCTkTextbox(ctk.CTkTextbox):
    """CTkTextbox that ignores unsupported tag font options."""

    _FORBIDDEN_TAG_OPTIONS = {"font", "ctk_font"}

    def tag_config(self, tagName, **kwargs):  # noqa: N802 (Tkinter camelCase)
        cleaned = {k: v for k, v in kwargs.items() if k not in self._FORBIDDEN_TAG_OPTIONS}
        return super().tag_config(tagName, **cleaned)

    def tag_configure(self, tagName, **kwargs):  # noqa: N802 (Tkinter camelCase)
        cleaned = {k: v for k, v in kwargs.items() if k not in self._FORBIDDEN_TAG_OPTIONS}
        return super().tag_configure(tagName, **cleaned)

# =========================
#  Captura global de erros
# =========================

def _show_fatal_error(exc: BaseException):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    try:
        log_path = os.path.join(os.path.dirname(__file__), "rn_error.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(tb)
    except Exception:
        pass
    try:
        _r = tk.Tk(); _r.withdraw()
        messagebox.showerror("Erro inesperado", tb)
        _r.destroy()
    except Exception:
        print(tb, file=sys.stderr)

sys.excepthook = lambda et, ev, tb: _show_fatal_error(ev)

# =========================
#  Setup visual do CTk
# =========================
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# =========================
#  Constantes do domínio
# =========================
CUR_L, CUR_R = "“", "”"

# UI do app permanece em PT-BR. As frases GERADAS mudam pelo idioma.
RESPONSAVEIS = ["Escritório Externo", "Jurídico Interno", "Texto livre…"]
SLA_TIPOS   = ["Dias úteis (fixo)", "Dias corridos (fixo)", "D- (antes do Marco)", "D+ (após o Marco)"]
GATILHOS    = [
    "Sempre que inserido novo OBJETO",
    "Em TAREFA se CAMPO for RESPOSTA",
    "Concluída TAREFA",
    "Após EVENTO",
]
OPERADORES  = ["é", "não é", "está preenchido", "está vazio", "está em", "foi respondido com"]

# =========================
#  i18n — Frases geradas (PT/ES)
# =========================
_LANG = "pt"  # padrão

TR = {
    "pt": {
        "when_new_object": "Sempre que inserido novo {obj}",
        "when_task_field_answer": "Na conclusão da tarefa {task}, se o campo {field} for respondido com {answer}",
        "when_task_done": "Concluída a tarefa {task}",
        "when_after_event": "Após {event}",
        "action_task": "é acionada a tarefa {task}",
        "action_resp": ", de responsabilidade do {resp}",
        "action_flow": "deverá ser acionado o fluxo de {flow}",
        # CORREÇÃO DE CONCORDÂNCIA: Substitui o gerúndio "atualizando" por voz passiva "o status é atualizado"
        "action_status": "o status é atualizado para {status}",
        "action_return": "o fluxo retornará a fase {task}{restart}",
        "restart_on": ", reiniciando seu SLA",
        "restart_off": "",
        # CORREÇÃO DE CONCORDÂNCIA: Substitui o gerúndio "encerrando" por voz passiva "o fluxo é encerrado"
        "closing_partial": "o fluxo é encerrado parcialmente",
        "closing_total": "o fluxo é encerrado totalmente",
        "unit_working_singular": "dia útil",
        "unit_working_plural": "dias úteis",
        "unit_calendar_singular": "dia corrido",
        "unit_calendar_plural": "dias corridos",
        "holidays_suffix": ", e considerando feriados",
        "sla_fixed_working": "com SLA de {n} {unit}, contados a partir de hoje{hol}",
        "sla_fixed_calendar": "com SLA de {n} {unit}, contados a partir de hoje",
        "sla_d_minus": "com SLA D-{n} em relação ao campo de data {marco}{hol}",
        "sla_d_plus": "com SLA de {n} {unit} após a {marco}{hol}",
        "and": " e ",
        "or": " ou ",
    },
    "es": {
        "when_new_object": "Siempre que se inserte un nuevo {obj}",
        "when_task_field_answer": "En la conclusión de la tarea {task}, si el campo {field} se responde con {answer}",
        "when_task_done": "Concluida la tarea {task}",
        "when_after_event": "Después de {event}",
        "action_task": "se activa la tarea {task}",
        "action_resp": ", a cargo de {resp}",
        "action_flow": "deberá activarse el flujo de {flow}",
        # CORREÇÃO DE CONCORDÂNCIA: Substitui o gerúndio "actualizando" por voz passiva "el estado se actualiza"
        "action_status": "el estado se actualiza a {status}",
        "action_return": "el flujo volverá a la fase {task}{restart}",
        "restart_on": ", reiniciando su SLA",
        "restart_off": "",
        # CORREÇÃO DE CONCORDÂNCIA: Substitui o gerúndio "cerrando" por voz passiva "el flujo se cierra"
        "closing_partial": "el flujo se cierra parcialmente",
        "closing_total": "el flujo se cierra totalmente",
        "unit_working_singular": "día hábil",
        "unit_working_plural": "días hábiles",
        "unit_calendar_singular": "día corrido",
        "unit_calendar_plural": "días corridos",
        "holidays_suffix": ", y considerando feriados",
        "sla_fixed_working": "con SLA de {n} {unit}, contados a partir de hoy{hol}",
        "sla_fixed_calendar": "con SLA de {n} {unit}, contados a partir de hoy",
        "sla_d_minus": "con SLA D-{n} con respecto al campo de fecha {marco}{hol}",
        "sla_d_plus": "con SLA de {n} {unit} después de {marco}{hol}",
        "and": " y ",
        "or": " o ",
    },
}

OPS_ES = {
    "é": "es",
    "não é": "no es",
    "está preenchido": "está lleno",
    "está vazio": "está vacío",
    "está em": "está en",
    "foi respondido com": "fue respondido con",
}

def set_lang(lang: str):
    global _LANG
    _LANG = "es" if str(lang).lower().startswith("es") else "pt"

def get_lang() -> str:
    return _LANG

def _t(key: str) -> str:
    pack = TR.get(get_lang(), TR["pt"])
    return pack.get(key, TR["pt"].get(key, key))

# =========================
#  Montagem textual
# =========================

def _plural_unit(kind: str, n: int) -> str:
    if kind == "working":
        return _t("unit_working_singular") if n == 1 else _t("unit_working_plural")
    else:
        return _t("unit_calendar_singular") if n == 1 else _t("unit_calendar_plural")

def _render_sla(tipo: str, dias: int, marco: str, feriados: bool) -> str:
    dias = int(dias)
    hol = _t("holidays_suffix") if feriados else ""
    if tipo.startswith("Dias úteis"):
        unit = _plural_unit("working", dias)
        return _t("sla_fixed_working").format(n=dias, unit=unit, hol=hol)
    if tipo.startswith("Dias corridos"):
        unit = _plural_unit("calendar", dias)
        return _t("sla_fixed_calendar").format(n=dias, unit=unit)
    if tipo.startswith("D- "):
        return _t("sla_d_minus").format(n=dias, marco=f"{CUR_L}{marco}{CUR_R}", hol=hol)
    if tipo.startswith("D+ "):
        unit = _plural_unit("working", dias)
        return _t("sla_d_plus").format(n=dias, unit=unit, marco=f"{CUR_L}{marco}{CUR_R}", hol=hol)
    return ""

def _join_conditions(conds, conj_flag: str) -> str:
    if not conds:
        return ""
    connector = _t("and") if conj_flag == "E" else _t("or")
    return connector.join(conds)

def _cond_to_text(campo: str, op: str, valor: str) -> str:
    lang = get_lang()
    cq = f"{CUR_L}{campo}{CUR_R}" if campo else ""
    if op in ("está preenchido", "está vazio"):
        if lang == "es":
            verbo = OPS_ES.get(op, op)
            return f"el campo {cq} {verbo}"
        return f"o campo {cq} {op}"
    if op == "está em":
        if lang == "es":
            return f"el campo {cq} {OPS_ES.get(op, op)} {CUR_L}{valor}{CUR_R}"
        return f"o campo {cq} está em {CUR_L}{valor}{CUR_R}"
    if lang == "es":
        verbo = OPS_ES.get(op, op)
        return f"el campo {cq} {verbo} {CUR_L}{valor}{CUR_R}"
    return f"o campo {cq} {op} {CUR_L}{valor}{CUR_R}"

def _acao_tarefa_texto(tarefa: str, responsavel: str, sla_txt: str) -> str:
    base = _t("action_task").format(task=f"{CUR_L}{tarefa}{CUR_R}")
    if responsavel:
        base += _t("action_resp").format(resp=responsavel)
    if sla_txt:
        base += f", {sla_txt}"
    return base

def _acao_status_texto(status: str) -> str:
    # A string agora é uma frase completa, com voz passiva: "o status é atualizado para..."
    return _t("action_status").format(status=f"{CUR_L}{status}{CUR_R}")

def _acao_fluxo_texto(fluxo: str) -> str:
    return _t("action_flow").format(flow=f"{CUR_L}{fluxo}{CUR_R}")

def _acao_retornar_texto(tarefa: str, reiniciar: bool) -> str:
    restart = _t("restart_on") if reiniciar else _t("restart_off")
    return _t("action_return").format(task=f"{CUR_L}{tarefa}{CUR_R}", restart=restart)

def _acao_encerramento(parcial: bool) -> str:
    # A string agora é uma frase completa, com voz passiva: "o fluxo é encerrado..."
    return _t("closing_partial") if parcial else _t("closing_total")

def _compose_rn(idx: int, when: str, cond: str, acoes: str) -> str:
    linha = f"RN{idx}: {when}"
    if cond:
        link = "e " if (" se " in when or " Se " in when) else "se "
        linha += f", {link}{cond}"
    linha += f", {acoes}." if acoes else "."
    return linha


# ==============================================
#  PARTE 2/6 — Widgets & Utilidades
# ==============================================

def group(parent, text, row, col=0, padx=10, pady=(10,6), sticky="we"):
    frame = ctk.CTkFrame(parent)
    frame.grid(row=row, column=col, sticky=sticky, padx=padx, pady=pady)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    title = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(weight="bold"))
    title.grid(row=0, column=0, sticky="w", padx=8, pady=(8,0))
    inner = ctk.CTkFrame(frame, fg_color="transparent")
    inner.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
    inner.grid_columnconfigure(0, weight=1)
    inner.grid_rowconfigure(1, weight=1)
    return inner


def scrollable_body(widget: ctk.CTkScrollableFrame):
    """Retorna o corpo real de um CTkScrollableFrame, compatível com versões antigas."""
    return getattr(widget, "scrollable_frame", getattr(widget, "_scrollable_frame", widget))

# REMOVIDO: ScrollFrame não é mais necessário com o CTkTabview
# def _capture_scroll(widget):
#     canvas = None
#     w = widget
#     while w is not None:
#         if hasattr(w, "_parent_canvas"):
#             canvas = w._parent_canvas
#             break
#         w = getattr(w, "master", None)
#     try:
#         return canvas, canvas.yview()[0]
#     except Exception:
#         return None, None

# def _restore_scroll(canvas, y, widget):
#     if canvas is not None and y is not None:
#         widget.after_idle(lambda: canvas.yview_moveto(y))

class IntSpin(ctk.CTkFrame):
    def __init__(self, master, from_=0, to=365, width=90, variable=None, on_change=None):
        super().__init__(master)
        self.min = from_; self.max = to
        self.on_change = on_change
        self.var = variable or tk.IntVar(value=0)
        ctk.CTkButton(self, text="−", width=28, command=self._dec).grid(row=0, column=0, padx=(0,2))
        self.entry = ctk.CTkEntry(self, width=width-56)
        self.entry.grid(row=0, column=1)
        ctk.CTkButton(self, text="+", width=28, command=self._inc).grid(row=0, column=2, padx=(2,0))
        self.entry.insert(0, str(self.var.get()))
        self.entry.bind("<FocusOut>", self._sync_from_entry)
        self.entry.bind("<Return>", self._sync_from_entry)

    def _clamp(self, v):
        return max(self.min, min(self.max, v))

    def _notify(self):
        if callable(self.on_change):
            self.on_change()

    def _sync_from_entry(self, *_):
        try:
            v = int(self.entry.get().strip())
        except Exception:
            v = self.var.get()
        v = self._clamp(v)
        if v != self.var.get():
            self.var.set(v)
        self.entry.delete(0, "end"); self.entry.insert(0, str(v))
        self._notify()

    def _dec(self):
        self.var.set(self._clamp(int(self.var.get()) - 1))
        self.entry.delete(0, "end"); self.entry.insert(0, str(self.var.get()))
        self._notify()

    def _inc(self):
        self.var.set(self._clamp(int(self.var.get()) + 1))
        self.entry.delete(0, "end"); self.entry.insert(0, str(self.var.get()))
        self._notify()

# REMOVIDO: ScrollFrame não é mais necessário com o CTkTabview
# class ScrollFrame(ctk.CTkScrollableFrame):
#     def __init__(self, master, height=300):
#         super().__init__(master, height=height)
#         self.grid_columnconfigure(0, weight=1)
#         self.body = self


class LinhaCondicao(ctk.CTkFrame):
    def __init__(self, master, on_change, on_remove):
        super().__init__(master)
        self.on_change = on_change
        self.on_remove = on_remove
        self.var_campo = tk.StringVar()
        self.var_op = tk.StringVar(value=OPERADORES[0])
        self.var_valor = tk.StringVar()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Campo:").grid(row=0, column=0, sticky="w", padx=4, pady=(2, 0))
        ctk.CTkEntry(self, textvariable=self.var_campo).grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 6))

        ctk.CTkLabel(self, text="Operador:").grid(row=2, column=0, sticky="w", padx=4, pady=(0, 0))
        ctk.CTkComboBox(
            self,
            values=OPERADORES,
            variable=self.var_op,
            command=lambda *_: self.on_change(),
        ).grid(row=3, column=0, sticky="ew", padx=4, pady=(0, 6))

        ctk.CTkLabel(self, text="Valor / Resposta:").grid(row=4, column=0, sticky="w", padx=4, pady=(0, 0))
        ctk.CTkEntry(self, textvariable=self.var_valor).grid(row=5, column=0, sticky="ew", padx=4, pady=(0, 6))

        # --- MELHORIA UX: Botões de reordenar ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=6, column=0, sticky="w", padx=4, pady=(0, 6))

        app = self.winfo_toplevel()
        ctk.CTkButton(
            btn_frame,
            text="↑",
            width=28,
            command=lambda: app._move_row(self, -1, app.cond_rows, app.frm_conds_body),
        ).pack(side="left", padx=(0, 2))
        ctk.CTkButton(
            btn_frame,
            text="↓",
            width=28,
            command=lambda: app._move_row(self, 1, app.cond_rows, app.frm_conds_body),
        ).pack(side="left", padx=(0, 4))
        ctk.CTkButton(btn_frame, text="Remover", command=self._remove, width=90).pack(side="left")
        # --- FIM MELHORIA UX ---

        for v in (self.var_campo, self.var_op, self.var_valor):
            v.trace_add("write", lambda *a: self.on_change())

    def _remove(self):
        try:
            self.destroy()
        finally:
            if callable(self.on_remove):
                self.on_remove(self)
            self.on_change()

    def request_remove(self):
        self._remove()

    def to_dict(self):
        return {"campo": self.var_campo.get(), "op": self.var_op.get(), "valor": self.var_valor.get()}

    def from_dict(self, d: dict):
        self.var_campo.set(d.get("campo", ""))
        self.var_op.set(d.get("op", OPERADORES[0]))
        self.var_valor.set(d.get("valor", ""))

    def to_text(self):
        c, o, v = self.var_campo.get().strip(), self.var_op.get(), self.var_valor.get().strip()
        if not c:
            return ""
        if o in ("é", "não é", "está em", "foi respondido com") and not v:
            return ""
        return _cond_to_text(c, o, v)


# ==============================================
#  PARTE 3/6 — LinhaAcao
# ==============================================

class LinhaAcao(ctk.CTkFrame):
    # --- MELHORIA UX: Adicionado row_list_key para reordenar ---
    def __init__(self, master, on_change, on_remove, default_resp="Escritório Externo", default_resp_free="", row_list_key="acao_rows"):
        super().__init__(master)
        self.on_change = on_change
        self.on_remove = on_remove
        self.row_list_key = row_list_key # Usado para reordenar a lista de ações no app

        self.var_tipo = tk.StringVar(value="Acionar Tarefa")

        self.var_tarefa = tk.StringVar()
        self.var_resp = tk.StringVar(value=("Escritório Externo" if default_resp in RESPONSAVEIS else "Texto livre…"))
        self.var_resp_livre = tk.StringVar(value=("" if default_resp in RESPONSAVEIS else default_resp))
        self.var_sla_tipo = tk.StringVar(value=SLA_TIPOS[0])
        self.var_sla_dias = tk.IntVar(value=2)
        self.var_sla_marco = tk.StringVar(value="Prazo Fatal da Peça")
        self.var_sla_fer = tk.BooleanVar(value=True)
        self.var_status = tk.StringVar()
        self.var_fluxo = tk.StringVar()
        self.var_texto = tk.StringVar()

        self.var_ret_tarefa = tk.StringVar()
        self.var_ret_restart = tk.BooleanVar(value=True)

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Tipo de ação:").grid(row=0, column=0, sticky="w", padx=4, pady=(2, 0))
        ctk.CTkComboBox(
            self,
            values=[
                "Acionar Tarefa",
                "Atualizar Status",
                "Acionar Fluxo",
                "Retornar a Tarefa",
                "Encerrar Fluxo (Parcial)",
                "Encerrar Fluxo (Total)",
                "Texto Livre",
            ],
            variable=self.var_tipo,
            command=lambda *_: self._refresh(),
        ).grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 6))

        self.frm_dyn = ctk.CTkFrame(self, fg_color="transparent")
        self.frm_dyn.grid(row=2, column=0, sticky="ew", padx=4, pady=(0, 4))
        self.frm_dyn.grid_columnconfigure(0, weight=1)

        # --- MELHORIA UX: Botões de reordenar ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, sticky="w", padx=4, pady=(0, 6))

        app = self.winfo_toplevel()
        # Pega a lista de ações correspondente no app (ex.: app.acao_rows)
        row_list = getattr(app, self.row_list_key, [])
        frame_parent = self.master  # container onde as ações são exibidas

        ctk.CTkButton(
            btn_frame,
            text="↑",
            width=28,
            command=lambda: app._move_row(self, -1, row_list, frame_parent),
        ).pack(side="left", padx=(0, 2))
        ctk.CTkButton(
            btn_frame,
            text="↓",
            width=28,
            command=lambda: app._move_row(self, 1, row_list, frame_parent),
        ).pack(side="left", padx=(0, 4))
        ctk.CTkButton(btn_frame, text="Remover", command=self._remove, width=90).pack(side="left")
        # --- FIM MELHORIA UX ---

        self._refresh()

    def _app(self):
        return self.winfo_toplevel()

    def _register_task_combo(self, combo, var_getter):
        try:
            self._app()._mem_register_task_combo(combo)
            self._app()._mem_bind_combo_capture(combo, var_getter, bucket="task")
        except Exception:
            pass

    def _register_field_combo(self, combo, var_getter):
        try:
            self._app()._mem_register_field_combo(combo)
            self._app()._mem_bind_combo_capture(combo, var_getter, bucket="field")
        except Exception:
            pass

    def _remove(self):
        try:
            self.destroy()
        finally:
            if callable(self.on_remove):
                self.on_remove(self)
            self.on_change()

    def request_remove(self):
        self._remove()

    def _refresh(self):
        # REMOVIDO: ScrollFrame não é mais necessário
        # canvas, y = _capture_scroll(self)
        for w in self.frm_dyn.winfo_children():
            w.destroy()
        t = self.var_tipo.get()

        if t == "Acionar Tarefa":
            row = 0
            ctk.CTkLabel(self.frm_dyn, text="Tarefa:").grid(row=row, column=0, sticky="w", pady=(0, 0))
            row += 1
            cb_tarefa = ctk.CTkComboBox(self.frm_dyn, values=self._app()._mem_get_tasks(), variable=self.var_tarefa)
            cb_tarefa.grid(row=row, column=0, sticky="ew", pady=(0, 6))
            self._register_task_combo(cb_tarefa, lambda: self.var_tarefa.get())
            row += 1

            ctk.CTkLabel(self.frm_dyn, text="Responsável:").grid(row=row, column=0, sticky="w")
            row += 1
            cb_resp = ctk.CTkComboBox(self.frm_dyn, values=RESPONSAVEIS, variable=self.var_resp)
            cb_resp.grid(row=row, column=0, sticky="ew", pady=(0, 4))
            row += 1
            self.entry_resp_livre = ctk.CTkEntry(self.frm_dyn, textvariable=self.var_resp_livre)

            def _toggle_resp(*_):
                if self.var_resp.get() == "Texto livre…":
                    self.entry_resp_livre.grid(row=row, column=0, sticky="ew", pady=(0, 6))
                else:
                    self.var_resp_livre.set("")
                    self.entry_resp_livre.grid_forget()
                self.on_change()

            cb_resp.configure(command=_toggle_resp)
            _toggle_resp()
            if self.entry_resp_livre.winfo_ismapped():
                row += 1

            ctk.CTkLabel(self.frm_dyn, text="Tipo de SLA:").grid(row=row, column=0, sticky="w")
            row += 1
            cb_sla = ctk.CTkComboBox(self.frm_dyn, values=SLA_TIPOS, variable=self.var_sla_tipo)
            cb_sla.grid(row=row, column=0, sticky="ew", pady=(0, 4))
            row += 1

            ctk.CTkLabel(self.frm_dyn, text="Dias:").grid(row=row, column=0, sticky="w")
            row += 1
            IntSpin(self.frm_dyn, from_=0, to=365, variable=self.var_sla_dias, width=120, on_change=self.on_change)\
                .grid(row=row, column=0, sticky="w", pady=(0, 4))
            row += 1

            self.chk_feriados = ctk.CTkCheckBox(
                self.frm_dyn,
                text="Considerar feriados",
                variable=self.var_sla_fer,
                onvalue=True,
                offvalue=False,
                command=self.on_change,
            )
            self.chk_feriados.grid(row=row, column=0, sticky="w", pady=(0, 4))
            row += 1

            self.lbl_marco = ctk.CTkLabel(self.frm_dyn, text="Campo de Data:")
            cb_marco = ctk.CTkComboBox(self.frm_dyn, values=self._app()._mem_get_fields(), variable=self.var_sla_marco)

            def _apply_sla_visibility(*_):
                tt = self.var_sla_tipo.get()
                is_corridos = (tt == "Dias corridos (fixo)")
                needs_marco = tt in ("D- (antes do Marco)", "D+ (após do Marco)")
                try:
                    self.chk_feriados.configure(state=("disabled" if is_corridos else "normal"))
                except Exception:
                    pass
                if needs_marco:
                    self.lbl_marco.grid(row=row, column=0, sticky="w")
                    cb_marco.grid(row=row + 1, column=0, sticky="ew", pady=(0, 4))
                    self._register_field_combo(cb_marco, lambda: self.var_sla_marco.get())
                else:
                    self.lbl_marco.grid_forget()
                    cb_marco.grid_forget()
                self.on_change()

            cb_sla.configure(command=_apply_sla_visibility)
            _apply_sla_visibility()
            if cb_marco.winfo_ismapped():
                row += 2

        elif t == "Atualizar Status":
            ctk.CTkLabel(self.frm_dyn, text="Status:").grid(row=0, column=0, sticky="w")
            ctk.CTkEntry(self.frm_dyn, textvariable=self.var_status).grid(row=1, column=0, sticky="ew", pady=(0, 4))

        elif t == "Acionar Fluxo":
            ctk.CTkLabel(self.frm_dyn, text="Fluxo:").grid(row=0, column=0, sticky="w")
            ctk.CTkEntry(self.frm_dyn, textvariable=self.var_fluxo).grid(row=1, column=0, sticky="ew", pady=(0, 4))

        elif t == "Retornar a Tarefa":
            ctk.CTkLabel(self.frm_dyn, text="Retornar a tarefa:").grid(row=0, column=0, sticky="w")
            cb_ret = ctk.CTkComboBox(self.frm_dyn, values=self._app()._mem_get_tasks(), variable=self.var_ret_tarefa)
            cb_ret.grid(row=1, column=0, sticky="ew", pady=(0, 4))
            self._register_task_combo(cb_ret, lambda: self.var_ret_tarefa.get())
            ctk.CTkCheckBox(
                self.frm_dyn,
                text="Reiniciar SLA",
                variable=self.var_ret_restart,
                onvalue=True,
                offvalue=False,
                command=self.on_change,
            ).grid(row=2, column=0, sticky="w", pady=(0, 4))

        # --- MELHORIA UX: Novo tipo de ação ---
        elif t.startswith("Encerrar Fluxo"):
            pass # Não precisa de widgets adicionais

        else: # Texto Livre
            ctk.CTkLabel(self.frm_dyn, text="Texto:").grid(row=0, column=0, sticky="w")
            ctk.CTkEntry(self.frm_dyn, textvariable=self.var_texto).grid(row=1, column=0, sticky="ew", pady=(0, 4))

        for v in (
            self.var_tarefa, self.var_resp, self.var_resp_livre, self.var_sla_tipo, self.var_sla_dias,
            self.var_sla_marco, self.var_sla_fer, self.var_status, self.var_fluxo, self.var_texto,
            self.var_ret_tarefa, self.var_ret_restart,
        ):
            try:
                v.trace_add("write", lambda *a: self.on_change())
            except Exception:
                pass

        self.on_change()
        # REMOVIDO: ScrollFrame não é mais necessário
        # _restore_scroll(canvas, y, self)

    def to_dict(self) -> dict:
        return {
            "tipo": self.var_tipo.get(),
            "tarefa": self.var_tarefa.get(),
            "resp": self.var_resp.get(),
            "resp_livre": self.var_resp_livre.get(),
            "sla_tipo": self.var_sla_tipo.get(),
            "sla_dias": int(self.var_sla_dias.get()),
            "sla_marco": self.var_sla_marco.get(),
            "sla_fer": bool(self.var_sla_fer.get()),
            "status": self.var_status.get(),
            "fluxo": self.var_fluxo.get(),
            "texto": self.var_texto.get(),
            "ret_tarefa": self.var_ret_tarefa.get(),
            "ret_restart": bool(self.var_ret_restart.get()),
        }

    def from_dict(self, d: dict):
        # --- MELHORIA UX: Migração de projetos antigos ---
        tipo = d.get("tipo", "Acionar Tarefa")
        texto = d.get("texto", "")

        # Migração de projetos antigos
        if tipo == "Texto Livre":
            if texto == _t("closing_partial"): # Usa a string i18n para comparar
                tipo = "Encerrar Fluxo (Parcial)"
            elif texto == _t("closing_total"):
                tipo = "Encerrar Fluxo (Total)"
        
        self.var_tipo.set(tipo); self._refresh()
        # --- FIM MELHORIA UX ---

        self.var_tarefa.set(d.get("tarefa", ""))
        self.var_resp.set(d.get("resp", "Escritório Externo"))
        self.var_resp_livre.set(d.get("resp_livre", ""))
        self.var_sla_tipo.set(d.get("sla_tipo", SLA_TIPOS[0])); self._refresh()
        self.var_sla_dias.set(int(d.get("sla_dias", 2)))
        self.var_sla_marco.set(d.get("sla_marco", "Prazo Fatal da Peça"))
        self.var_sla_fer.set(bool(d.get("sla_fer", True)))
        self.var_status.set(d.get("status", ""))
        self.var_fluxo.set(d.get("fluxo", ""))
        self.var_texto.set(d.get("texto", ""))
        self.var_ret_tarefa.set(d.get("ret_tarefa", ""))
        self.var_ret_restart.set(bool(d.get("ret_restart", True)))
        self._refresh()

    def to_text(self) -> str:
        t = self.var_tipo.get()
        if t == "Acionar Tarefa":
            tarefa = self.var_tarefa.get().strip()
            if not tarefa:
                return ""
            resp = self.var_resp.get()
            if resp == "Texto livre…":
                resp = self.var_resp_livre.get().strip()
            sla = _render_sla(self.var_sla_tipo.get(), int(self.var_sla_dias.get()),
                              self.var_sla_marco.get().strip(), bool(self.var_sla_fer.get()))
            return _acao_tarefa_texto(tarefa, resp, sla)
        if t == "Atualizar Status":
            st = self.var_status.get().strip()
            # Esta função retorna a nova string corrigida (ex: "o status é atualizado para...")
            return _acao_status_texto(st) if st else ""
        if t == "Acionar Fluxo":
            fx = self.var_fluxo.get().strip()
            return _acao_fluxo_texto(fx) if fx else ""
        if t == "Retornar a Tarefa":
            return _acao_retornar_texto(self.var_ret_tarefa.get().strip(), bool(self.var_ret_restart.get()))
        
        # --- MELHORIA UX: Novos tipos de ação ---
        if t == "Encerrar Fluxo (Parcial)":
            return _acao_encerramento(parcial=True)
        if t == "Encerrar Fluxo (Total)":
            return _acao_encerramento(parcial=False)
        # --- FIM MELHORIA UX ---

        tx = self.var_texto.get().strip()
        # Se for Texto Livre e o usuário digitar 'encerrando...', ele ainda pode quebrar a concordância
        # mas o uso dos botões rápidos e a ação de Texto Livre agora usam a nova frase corrigida.
        return tx if tx else ""


# ==============================================
#  PARTE 4/6 — RNBuilder (cabeçalho, memórias, idioma, salvar/abrir)
# ==============================================

class RNBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RN Builder — Montador de Regras")
        self.geometry("1280x860")
        self.minsize(1120, 800)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.rns: list[str] = []
        self.start_idx = tk.IntVar(value=1)

        self._mem_tasks: list[str] = []
        self._mem_fields: list[str] = []
        self._task_combos: list = []
        self._field_combos: list = []
        self._mem_guard = False

        self.var_resp_preset = tk.StringVar(value="Escritório Externo")
        self.var_resp_preset_free = tk.StringVar()

        self._lang_var = tk.StringVar(value=("Português" if get_lang() == "pt" else "Español"))

        self._build_header()

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=9, minsize=420)
        self.content.grid_columnconfigure(1, weight=11, minsize=520)

        self._bind_shortcuts()

    # Memória de combos
    def _norm(self, s: str) -> str:
        return " ".join((s or "").split()).strip()

    def _add_unique(self, bucket_list: list, value: str):
        v = self._norm(value)
        if len(v) < 3:
            return
        if any(v.lower() == x.lower() for x in bucket_list):
            return
        bucket_list.append(v)

    def _mem_add_task(self, s: str):
        before = len(self._mem_tasks)
        self._add_unique(self._mem_tasks, s)
        if len(self._mem_tasks) != before:
            self._refresh_task_combos()

    def _mem_add_field(self, s: str):
        before = len(self._mem_fields)
        self._add_unique(self._mem_fields, s)
        if len(self._mem_fields) != before:
            self._refresh_field_combos()

    def _mem_get_tasks(self):
        return list(self._mem_tasks)

    def _mem_get_fields(self):
        return list(self._mem_fields)

    def _mem_register_task_combo(self, combo):
        try:
            if combo not in self._task_combos:
                self._task_combos.append(combo)
            combo.configure(values=self._mem_get_tasks())
        except Exception:
            pass

    def _mem_register_field_combo(self, combo):
        try:
            if combo not in self._field_combos:
                self._field_combos.append(combo)
            combo.configure(values=self._mem_get_fields())
        except Exception:
            pass

    def _refresh_task_combos(self):
        if self._mem_guard:
            return
        self._mem_guard = True
        try:
            vals = self._mem_get_tasks()
            for cb in list(self.task_combos):
                try:
                    cb.configure(values=vals)
                except Exception:
                    pass
        finally:
            self._mem_guard = False

    def _refresh_field_combos(self):
        if self._mem_guard:
            return
        self._mem_guard = True
        try:
            vals = self._mem_get_fields()
            for cb in list(self.field_combos):
                try:
                    cb.configure(values=vals)
                except Exception:
                    pass
        finally:
            self._mem_guard = False

    def _mem_bind_combo_capture(self, combo, getter, bucket: str):
        try:
            entry = combo._entry
            if bucket == "task":
                entry.bind("<FocusOut>", lambda e: self._mem_add_task(getter()))
                entry.bind("<Return>",   lambda e: self._mem_add_task(getter()))
            else:
                entry.bind("<FocusOut>", lambda e: self._mem_add_field(getter()))
                entry.bind("<Return>",   lambda e: self._mem_add_field(getter()))
        except Exception:
            pass

        def _on_select(_=None):
            if self._mem_guard:
                return
            try:
                self._mem_guard = True
                val = getter()
                if bucket == "task":
                    self._mem_add_task(val)
                else:
                    self._mem_add_field(val)
            finally:
                self._mem_guard = False
        try:
            combo.configure(command=_on_select)
        except Exception:
            pass

    def _clear_memories(self):
        if messagebox.askyesno("Limpar memórias", "Limpar listas de TAREFAS e CAMPOS deste projeto?"):
            self._mem_tasks.clear(); self._mem_fields.clear()
            self._refresh_task_combos(); self._refresh_field_combos()
    
    # --- MELHORIA UX: Stub para gerenciador de listas ---
    def _open_mem_manager(self):
        # TODO: Implementar gerenciador de listas em um CTkToplevel
        messagebox.showinfo("Em breve", "O gerenciador de listas será implementado aqui.")

    # Cabeçalho
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="we", padx=10, pady=(10, 6))
        header.grid_columnconfigure(0, weight=1)

        button_bar = ctk.CTkFrame(header, fg_color="transparent")
        button_bar.grid(row=0, column=0, sticky="we")

        actions_bar = ctk.CTkFrame(button_bar, fg_color="transparent")
        actions_bar.pack(side="left", fill="x", expand=True)
        for text, cmd, width in (
            ("Limpar construtor", self._clear_builder, 150),
            ("Gerenciar Listas", self._open_mem_manager, 160),
            ("Limpar memórias", self._clear_memories, 150),
            ("Reset geral", self._reset_all, 140),
        ):
            ctk.CTkButton(actions_bar, text=text, command=cmd, width=width).pack(side="left", padx=(0, 8), pady=4)

        more_bar = ctk.CTkFrame(button_bar, fg_color="transparent")
        more_bar.pack(side="right")
        ctk.CTkLabel(more_bar, text="Idioma:").pack(side="left", padx=(0, 6))
        ctk.CTkOptionMenu(
            more_bar,
            values=["Português", "Español"],
            variable=self._lang_var,
            width=120,
            command=self._on_change_lang,
        ).pack(side="left", padx=(0, 12))

        self._more_btn = ctk.CTkButton(more_bar, text="Mais...", command=self._open_more_menu, width=140)
        self._more_btn.pack(side="left")

        config_row = ctk.CTkFrame(header, fg_color="transparent")
        config_row.grid(row=1, column=0, sticky="we", pady=(6, 0))
        config_row.grid_columnconfigure(2, weight=1)

        start_frame = ctk.CTkFrame(config_row, fg_color="transparent")
        start_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(start_frame, text="RN inicial:").pack(side="left", padx=(0, 6))
        self.spin_start = IntSpin(start_frame, from_=1, to=999, width=110, variable=self.start_idx)
        self.spin_start.pack(side="left")
        def _sync_start(*_):
            try:
                value = int(self.start_idx.get())
            except Exception:
                value = 1
            self.spin_start.entry.delete(0, "end")
            self.spin_start.entry.insert(0, str(value))
        self.start_idx.trace_add("write", lambda *a: _sync_start())
        _sync_start()

        resp_frame = ctk.CTkFrame(config_row, fg_color="transparent")
        resp_frame.grid(row=0, column=1, sticky="w", padx=(20, 0))
        ctk.CTkLabel(resp_frame, text="Responsável padrão (novas ações):").pack(side="left")

        cb = ctk.CTkComboBox(
            resp_frame,
            values=["Escritório Externo", "Jurídico Interno", "Texto livre…"],
            variable=self.var_resp_preset,
            width=220,
        )
        cb.pack(side="left", padx=(6, 0))

        self.entry_resp_preset_free = ctk.CTkEntry(
            resp_frame, textvariable=self.var_resp_preset_free, width=220
        )

        def _toggle_preset_free(*_):
            if self.var_resp_preset.get() == "Texto livre…":
                self.entry_resp_preset_free.pack(side="left", padx=(6, 0))
            else:
                self.var_resp_preset_free.set("")
                try:
                    self.entry_resp_preset_free.pack_forget()
                except Exception:
                    pass

        cb.configure(command=_toggle_preset_free)
        _toggle_preset_free()

    def _on_change_lang(self, _choice: str):
        val = self._lang_var.get()
        set_lang("es" if val.startswith("Espa") else "pt")
        try:
            if hasattr(self, "_update_preview"):
                self._update_preview()
        except Exception:
            pass

    def _open_more_menu(self):
        try:
            menu = tk.Menu(self, tearoff=False)
            menu.add_command(label="Salvar projeto…", command=self._save_project)
            menu.add_command(label="Abrir projeto…", command=self._open_project)
            menu.add_separator()
            menu.add_command(label="Sobre", command=self._show_about)
            bx = self._more_btn.winfo_rootx()
            by = self._more_btn.winfo_rooty() + self._more_btn.winfo_height()
            try:
                menu.tk_popup(bx, by)
            finally:
                menu.grab_release()
        except Exception as e:
            messagebox.showerror("Menu", str(e))

    def _bind_shortcuts(self):
        try:
            self.bind_all("<Control-s>", lambda e: self._save_project())
            self.bind_all("<Control-o>", lambda e: self._open_project())
            self.bind_all("<Control-L>", lambda e: self._clear_builder())
            self.bind_all("<Control-l>", lambda e: self._clear_builder())
            self.bind_all("<Control-M>", lambda e: self._clear_memories())
            self.bind_all("<Control-m>", lambda e: self._clear_memories())
            self.bind_all("<Control-Shift-R>", lambda e: self._reset_all())
            self.bind_all("<F1>", lambda e: self._show_about())

            # --- MELHORIA UX: Novos atalhos ---
            self.bind_all("<Control-Return>", lambda e: self._add_rn())
            self.bind_all("<Alt-c>", lambda e: self._add_cond())
            self.bind_all("<Alt-a>", lambda e: self._add_acao())
            # --- FIM MELHORIA UX ---

        except Exception:
            pass

    def _show_about(self):
        messagebox.showinfo("Sobre", "Criado por Rodrigo Salvador Escudero")

    def _clear_header(self):
        self.start_idx.set(1)
        self.var_resp_preset.set("Escritório Externo")
        self.var_resp_preset_free.set("")
        try:
            self.entry_resp_preset_free.pack_forget()
        except Exception:
            pass

    def _clear_builder(self):
        try:
            if hasattr(self, "_destroy_rows"):
                self._destroy_rows(getattr(self, "cond_rows", []))
                self._destroy_rows(getattr(self, "acao_rows", []))
                if hasattr(self, "_ensure_min_builder_rows"):
                    self._ensure_min_builder_rows()
            if hasattr(self, "_update_preview"):
                self._update_preview()
        except Exception:
            pass

    def _reset_all(self):
        self._clear_header()
        self._mem_tasks.clear(); self._mem_fields.clear()
        self._refresh_task_combos(); self._refresh_field_combos()
        try:
            if hasattr(self, "_reset_builder_defaults"):
                self._reset_builder_defaults()
            if hasattr(self, "_clear_rns"):
                self._clear_rns(confirm=False)
            if hasattr(self, "_clear_preview"):
                self._clear_preview()
            if hasattr(self, "_update_preview"):
                self._update_preview()
            if hasattr(self, "_ensure_min_builder_rows"):
                self._ensure_min_builder_rows()
        except Exception:
            pass

    # Persistência
    def _collect_project(self) -> dict:
        proj = {
            "version": 4,
            "lang": get_lang(),
            "header": {
                "start_idx": int(self.start_idx.get()),
                "resp_preset": self.var_resp_preset.get(),
                "resp_preset_free": self.var_resp_preset_free.get(),
            },
            "builder": {},
            "memory": {"tarefas": list(self._mem_tasks), "campos": list(self._mem_fields)},
            "rns": list(self.rns),
        }
        try:
            if hasattr(self, "_collect_builder_into"):
                self._collect_builder_into(proj)
        except Exception:
            pass
        return proj

    def _apply_project(self, proj: dict):
        try:
            lang = proj.get("lang", "pt")
            set_lang(lang)
            self._lang_var.set("Español" if lang == "es" else "Português")

            header = proj.get("header", {})
            self.start_idx.set(int(header.get("start_idx", 1)))
            self.var_resp_preset.set(header.get("resp_preset", "Escritório Externo"))
            self.var_resp_preset_free.set(header.get("resp_preset_free", ""))
            if self.var_resp_preset.get() == "Texto livre…":
                self.entry_resp_preset_free.pack(side="left", padx=(6, 0))
            else:
                try:
                    self.entry_resp_preset_free.pack_forget()
                except Exception:
                    pass

            mem = proj.get("memory", {})
            self._mem_tasks = list(mem.get("tarefas", []))
            self._mem_fields = list(mem.get("campos", []))
            self._refresh_task_combos(); self._refresh_field_combos()

            try:
                if hasattr(self, "_apply_builder_from"):
                    self._apply_builder_from(proj)
            except Exception:
                pass

            self.rns = list(proj.get("rns", []))
            try:
                if hasattr(self, "_refresh_textbox"):
                    self._refresh_textbox()
            except Exception:
                pass

            try:
                if hasattr(self, "_update_preview"):
                    self._update_preview()
            except Exception:
                pass

        except Exception as e:
            messagebox.showerror("Erro ao carregar projeto", str(e))

    def _save_project(self):
        proj = self._collect_project()
        path = filedialog.asksaveasfilename(
            title="Salvar projeto",
            defaultextension=".rnproj",
            filetypes=[("Projeto de RNs", ".rnproj"), ("JSON", ".json"), ("Todos", "*.*")],
            initialfile="meu_projeto.rnproj",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(proj, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Projeto salvo", f"Projeto salvo em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar projeto", str(e))

    def _open_project(self):
        path = filedialog.askopenfilename(
            title="Abrir projeto",
            filetypes=[("Projeto de RNs", ".rnproj"), ("JSON", ".json"), ("Todos", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                proj = json.load(f)
            self._apply_project(proj)
        except Exception as e:
            messagebox.showerror("Erro ao abrir projeto", str(e))


# ==============================================
#  PARTE 5/6 — Construtor (miolo)
# ==============================================

def _attach_builder_to_RNBuilder():
    def _build_rule(self: 'RNBuilder'):
        parent = getattr(self, "content", self)
        self.builder_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.builder_scroll.grid(row=0, column=1, sticky="nsew", padx=(6, 10), pady=6)
        self.builder_scroll.grid_columnconfigure(0, weight=1)

        self.builder_container = scrollable_body(self.builder_scroll)
        self.builder_container.grid_columnconfigure(0, weight=1)
        self.builder_container.grid_rowconfigure(0, weight=5)
        self.builder_container.grid_rowconfigure(1, weight=4)
        self.builder_container.grid_rowconfigure(2, weight=6)

        frm_gatilho_group = group(
            self.builder_container,
            "Gatilho",
            row=0,
            col=0,
            padx=(0, 0),
            pady=(0, 10),
            sticky="nsew",
        )
        frm_gatilho_group.grid_columnconfigure(0, weight=1)

        self.var_gatilho_tipo = tk.StringVar(value=GATILHOS[1])
        gtbar = ctk.CTkFrame(frm_gatilho_group, fg_color="transparent")
        gtbar.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        gtbar.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(gtbar, text="Gatilho:").grid(row=0, column=0, sticky="w")
        ctk.CTkComboBox(
            gtbar,
            values=GATILHOS,
            variable=self.var_gatilho_tipo,
            command=lambda *_: self._refresh_gatilho_fields(),
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        self.var_obj = tk.StringVar(value="Cadastro ou Pré Cadastro")
        self.var_tarefa_ctx = tk.StringVar(value="Validar Nota Fiscal")
        self.var_campo = tk.StringVar(value="Nota aprovada?")
        self.var_resposta = tk.StringVar(value="Não")
        self.var_tarefa_done = tk.StringVar(value="Realizar Protocolo da Peça e Anexar Comprovante")
        self.var_evento = tk.StringVar(value="Prazo Fatal da Peça atingido")

        self.frm_gatilho = ctk.CTkFrame(frm_gatilho_group, fg_color="transparent")
        self.frm_gatilho.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))
        self.frm_gatilho.grid_columnconfigure(0, weight=1)
        self._refresh_gatilho_fields()

        frm_cond_group = group(
            self.builder_container,
            "Condições adicionais",
            row=1,
            col=0,
            padx=(0, 0),
            pady=(0, 10),
            sticky="nsew",
        )
        frm_cond_group.grid_columnconfigure(0, weight=1)

        cond_hdr = ctk.CTkFrame(frm_cond_group, fg_color="transparent")
        cond_hdr.grid(row=0, column=0, padx=6, pady=(6, 2), sticky="ew")
        cond_hdr.grid_columnconfigure(0, weight=1)
        cond_hdr.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(cond_hdr, text="Condições adicionais:").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        self.var_conj = tk.StringVar(value="E")
        ctk.CTkRadioButton(
            cond_hdr,
            text="Todas (E)",
            variable=self.var_conj,
            value="E",
            command=self._update_preview,
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))
        ctk.CTkRadioButton(
            cond_hdr,
            text="Qualquer (OU)",
            variable=self.var_conj,
            value="OU",
            command=self._update_preview,
        ).grid(row=1, column=1, sticky="w", pady=(4, 0), padx=(12, 0))

        self.frm_conds = ctk.CTkScrollableFrame(frm_cond_group, fg_color="transparent", height=240)
        self.frm_conds.grid(row=1, column=0, sticky="nsew", padx=6)
        self.frm_conds.grid_columnconfigure(0, weight=1)
        self.frm_conds_body = scrollable_body(self.frm_conds)
        self.frm_conds_body.grid_columnconfigure(0, weight=1)
        self.cond_rows = []

        cond_btnbar = ctk.CTkFrame(frm_cond_group, fg_color="transparent")
        cond_btnbar.grid(row=2, column=0, padx=6, pady=(4, 6), sticky="ew")
        cond_btnbar.grid_columnconfigure(0, weight=1)
        cond_btnbar.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(
            cond_btnbar,
            text="+ Adicionar condição",
            command=self._add_cond,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(
            cond_btnbar,
            text="Limpar condições",
            command=self._clear_conditions,
        ).grid(row=0, column=1, sticky="ew")

        frm_acao_group = group(
            self.builder_container,
            "Ações (então) e Ações Frequentes",
            row=2,
            col=0,
            padx=(0, 0),
            pady=(0, 0),
            sticky="nsew",
        )
        frm_acao_group.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frm_acao_group, text="Ações (então):").grid(row=0, column=0, padx=6, pady=(6,2), sticky="w")
        self.frm_acoes = ctk.CTkScrollableFrame(frm_acao_group, fg_color="transparent", height=260)
        self.frm_acoes.grid(row=1, column=0, sticky="nsew", padx=6)
        self.frm_acoes.grid_columnconfigure(0, weight=1)
        self.frm_acoes_body = scrollable_body(self.frm_acoes)
        self.frm_acoes_body.grid_columnconfigure(0, weight=1)
        self.acao_rows = []

        acoes_btnbar = ctk.CTkFrame(frm_acao_group, fg_color="transparent")
        acoes_btnbar.grid(row=2, column=0, padx=6, pady=(4, 2), sticky="ew")
        acoes_btnbar.grid_columnconfigure(0, weight=1)
        acoes_btnbar.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(
            acoes_btnbar,
            text="+ Adicionar ação",
            command=self._add_acao,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkButton(
            acoes_btnbar,
            text="Limpar ações",
            command=self._clear_actions,
        ).grid(row=0, column=1, sticky="ew")

        freq_bar = ctk.CTkFrame(frm_acao_group, fg_color="transparent")
        freq_bar.grid(row=3, column=0, padx=6, pady=(8, 4), sticky="ew")
        freq_bar.grid_columnconfigure(0, weight=1)
        freq_bar.grid_columnconfigure(1, weight=0)
        ctk.CTkLabel(freq_bar, text="Ações frequentes — Acionar fluxo:").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        self.var_freq = tk.StringVar(value="Cadastro")
        flow_combo = ctk.CTkComboBox(
            freq_bar,
            values=[
                "Cadastro",
                "Acordo",
                "Decisão",
                "Réplica",
                "Garantias",
                "Bloqueio",
                "Penhora",
                "Encerramento",
                "Reativação",
                "Perícias",
                "Obrigações",
            ],
            variable=self.var_freq,
        )
        flow_combo.grid(row=1, column=0, sticky="ew", pady=(4, 0), padx=(0, 6))
        ctk.CTkButton(
            freq_bar,
            text="Inserir",
            command=self._insert_frequent_flow,
        ).grid(row=1, column=1, sticky="ew", pady=(4, 0))

        freq_ret = ctk.CTkFrame(frm_acao_group, fg_color="transparent")
        freq_ret.grid(row=4, column=0, padx=6, pady=(2, 4), sticky="ew")
        freq_ret.grid_columnconfigure(0, weight=1)
        freq_ret.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(freq_ret, text="Retornar a tarefa:").grid(row=0, column=0, columnspan=2, sticky="w")
        self.var_freq_ret = tk.StringVar(value="")
        cb_ret = ctk.CTkComboBox(freq_ret, values=self._mem_get_tasks(), variable=self.var_freq_ret)
        cb_ret.grid(row=1, column=0, sticky="ew", pady=(4, 0), padx=(0, 6))
        self._mem_register_task_combo(cb_ret)
        self._mem_bind_combo_capture(cb_ret, lambda: self.var_freq_ret.get(), bucket="task")
        btn_ret = ctk.CTkButton(freq_ret, text="Inserir", command=self._insert_frequent_return)
        btn_ret.grid(row=1, column=1, sticky="ew", pady=(4, 0))
        self.var_freq_ret_restart = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            freq_ret,
            text="Reiniciar SLA",
            variable=self.var_freq_ret_restart,
            onvalue=True,
            offvalue=False,
            command=self._update_preview,
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))

        freq_cond = ctk.CTkFrame(frm_acao_group, fg_color="transparent")
        freq_cond.grid(row=5, column=0, padx=6, pady=(2, 6), sticky="ew")
        freq_cond.grid_columnconfigure(0, weight=1)
        freq_cond.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(freq_cond, text="Condição rápida (Campo / Resposta):").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ctk.CTkLabel(freq_cond, text="Campo:").grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.var_freq_cond_field = tk.StringVar(value="")
        cb_field = ctk.CTkComboBox(
            freq_cond,
            values=self._mem_get_fields(),
            variable=self.var_freq_cond_field,
        )
        cb_field.grid(row=1, column=1, sticky="ew", pady=(4, 0))
        self._mem_register_field_combo(cb_field)
        self._mem_bind_combo_capture(cb_field, lambda: self.var_freq_cond_field.get(), bucket="field")
        ctk.CTkLabel(freq_cond, text="Resposta:").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.var_freq_cond_resp = tk.StringVar(value="")
        ent_resp = ctk.CTkEntry(freq_cond, textvariable=self.var_freq_cond_resp)
        ent_resp.grid(row=2, column=1, sticky="ew", pady=(6, 0))
        ent_resp.bind("<Return>", lambda e: self._insert_frequent_condition())
        ent_resp.bind("<FocusOut>", lambda e: self._update_preview())
        ctk.CTkButton(
            freq_cond,
            text="Adicionar",
            command=self._insert_frequent_condition,
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        if not self.cond_rows:
            self._add_cond()
        if not self.acao_rows:
            self._add_acao()

        for v in (
            self.var_gatilho_tipo, self.var_obj, self.var_tarefa_ctx, self.var_campo,
            self.var_resposta, self.var_tarefa_done, self.var_evento, self.var_conj
        ):
            v.trace_add("write", lambda *a: self._update_preview())

    def _reset_builder_defaults(self: 'RNBuilder'):
        self.var_gatilho_tipo.set(GATILHOS[1])
        self.var_obj.set("Cadastro ou Pré Cadastro")
        self.var_tarefa_ctx.set("Validar Nota Fiscal")
        self.var_campo.set("Nota aprovada?")
        self.var_resposta.set("Não")
        self.var_tarefa_done.set("Realizar Protocolo da Peça e Anexar Comprovante")
        self.var_evento.set("Prazo Fatal da Peça atingido")
        self._refresh_gatilho_fields()

    def _destroy_rows(self: 'RNBuilder', rows):
        for r in list(rows):
            try:
                r.destroy()
            except Exception:
                pass
        rows.clear()

    def _relayout_cond_rows(self: 'RNBuilder'):
        for idx, widget in enumerate(getattr(self, 'cond_rows', [])):
            try:
                widget.grid(row=idx, column=0, sticky="ew", padx=0, pady=(0, 8))
            except Exception:
                pass

    def _relayout_acao_rows(self: 'RNBuilder'):
        for idx, widget in enumerate(getattr(self, 'acao_rows', [])):
            try:
                widget.grid(row=idx, column=0, sticky="ew", padx=0, pady=(0, 10))
            except Exception:
                pass

    def _ensure_min_builder_rows(self: 'RNBuilder'):
        try:
            if hasattr(self, 'frm_conds_body') and not getattr(self, 'cond_rows', []):
                self._add_cond()
            if hasattr(self, 'frm_acoes_body') and not getattr(self, 'acao_rows', []):
                self._add_acao()
        except Exception:
            pass

    def _clear_conditions(self: 'RNBuilder', *, confirm=True):
        if not getattr(self, 'cond_rows', []):
            if hasattr(self, 'frm_conds_body'):
                self._add_cond()
            return
        if (not confirm) or messagebox.askyesno("Limpar condições", "Remover todas as condições?"):
            self._destroy_rows(self.cond_rows)
            if hasattr(self, 'frm_conds_body'):
                self._add_cond()

    def _clear_actions(self: 'RNBuilder', *, confirm=True):
        if not getattr(self, 'acao_rows', []):
            if hasattr(self, 'frm_acoes_body'):
                self._add_acao()
            return
        if (not confirm) or messagebox.askyesno("Limpar ações", "Remover todas as ações?"):
            self._destroy_rows(self.acao_rows)
            if hasattr(self, 'frm_acoes_body'):
                self._add_acao()

    def _add_cond(self: 'RNBuilder'):
        def _on_remove(row):
            if row in self.cond_rows:
                self.cond_rows.remove(row)
                self._relayout_cond_rows()
            self.after_idle(self._ensure_min_builder_rows)

        row = LinhaCondicao(
            self.frm_conds_body,
            on_change=self._update_preview,
            on_remove=_on_remove,
        )
        self.cond_rows.append(row)
        self._relayout_cond_rows()
        self._update_preview()

    def _add_acao(self: 'RNBuilder'):
        preset_value = (self.var_resp_preset_free.get().strip() if self.var_resp_preset.get() == "Texto livre…"
                        else self.var_resp_preset.get())
        def _on_remove(row):
            if row in self.acao_rows:
                self.acao_rows.remove(row)
                self._relayout_acao_rows()
            self.after_idle(self._ensure_min_builder_rows)

        row = LinhaAcao(self.frm_acoes_body, on_change=self._update_preview,
                        on_remove=_on_remove,
                        default_resp=preset_value,
                        default_resp_free=self.var_resp_preset_free.get(),
                        row_list_key="acao_rows") # Passando a chave da lista
        self.acao_rows.append(row)
        self._relayout_acao_rows()
        self._update_preview()

    def _insert_frequent_flow(self: 'RNBuilder'):
        try:
            nome = (self.var_freq.get() or '').strip()
            if not nome:
                return
            preset_value = (self.var_resp_preset_free.get().strip() if self.var_resp_preset.get() == "Texto livre…"
                            else self.var_resp_preset.get())
            def _remove(row):
                if row in self.acao_rows:
                    self.acao_rows.remove(row)
                    self._relayout_acao_rows()
                    self.after_idle(self._ensure_min_builder_rows)

            row = LinhaAcao(self.frm_acoes_body, on_change=self._update_preview,
                            on_remove=_remove,
                            default_resp=preset_value, default_resp_free=self.var_resp_preset_free.get(),
                            row_list_key="acao_rows") # Passando a chave da lista
            row.var_tipo.set("Acionar Fluxo"); row._refresh(); row.var_fluxo.set(nome)
            self.acao_rows.append(row)
            self._relayout_acao_rows()
            self._update_preview()
        except Exception as e:
            messagebox.showerror("Falha ao inserir ação frequente", str(e))

    def _insert_frequent_return(self: 'RNBuilder'):
        try:
            tarefa = (self.var_freq_ret.get() or '').strip()
            if not tarefa:
                return
            self._mem_add_task(tarefa)
            preset_value = (self.var_resp_preset_free.get().strip() if self.var_resp_preset.get() == "Texto livre…"
                            else self.var_resp_preset.get())
            def _remove(row):
                if row in self.acao_rows:
                    self.acao_rows.remove(row)
                    self._relayout_acao_rows()
                    self.after_idle(self._ensure_min_builder_rows)

            row = LinhaAcao(self.frm_acoes_body, on_change=self._update_preview,
                            on_remove=_remove,
                            default_resp=preset_value, default_resp_free=self.var_resp_preset_free.get(),
                            row_list_key="acao_rows") # Passando a chave da lista
            row.var_tipo.set("Retornar a Tarefa"); row._refresh()
            row.var_ret_tarefa.set(tarefa)
            row.var_ret_restart.set(bool(self.var_freq_ret_restart.get()))
            self.acao_rows.append(row)
            self._relayout_acao_rows()
            self._update_preview()
        except Exception as e:
            messagebox.showerror("Falha ao inserir 'Retornar a tarefa'", str(e))

    def _insert_frequent_condition(self: 'RNBuilder'):
        try:
            campo = (self.var_freq_cond_field.get() or '').strip()
            resp  = (self.var_freq_cond_resp.get() or '').strip()
            if not campo or not resp:
                messagebox.showwarning("Condição incompleta", "Informe o Campo e a Resposta.")
                return
            self._mem_add_field(campo)
            def _remove(row):
                if row in self.cond_rows:
                    self.cond_rows.remove(row)
                    self._relayout_cond_rows()
                    self.after_idle(self._ensure_min_builder_rows)

            row = LinhaCondicao(self.frm_conds_body, on_change=self._update_preview,
                                on_remove=_remove)
            row.var_campo.set(campo)
            row.var_op.set("foi respondido com")
            row.var_valor.set(resp)
            self.cond_rows.append(row)
            self._relayout_cond_rows()
            self._update_preview()
        except Exception as e:
            messagebox.showerror("Falha ao inserir condição rápida", str(e))

    # --- MELHORIA UX: Função removida pois os botões foram removidos ---
    # def _insert_frequent_close(self: 'RNBuilder', *, parcial: bool):
    #     ...

    def _refresh_gatilho_fields(self: 'RNBuilder'):
        # REMOVIDO: ScrollFrame não é mais necessário
        # canvas, y = _capture_scroll(self)
        for w in self.frm_gatilho.winfo_children():
            w.destroy()
        for col in range(2):
            self.frm_gatilho.grid_columnconfigure(col, weight=(0 if col == 0 else 1))
        t = self.var_gatilho_tipo.get()
        if t == "Sempre que inserido novo OBJETO":
            ctk.CTkLabel(self.frm_gatilho, text="Objeto:").grid(
                row=0, column=0, padx=(0, 6), pady=3, sticky="w"
            )
            ctk.CTkEntry(self.frm_gatilho, textvariable=self.var_obj).grid(
                row=0, column=1, padx=(0, 0), pady=3, sticky="ew"
            )
        elif t == "Em TAREFA se CAMPO for RESPOSTA":
            ctk.CTkLabel(self.frm_gatilho, text="Tarefa:").grid(
                row=0, column=0, padx=(0, 6), pady=3, sticky="w"
            )
            cb_t = ctk.CTkComboBox(
                self.frm_gatilho,
                values=self._mem_get_tasks(),
                variable=self.var_tarefa_ctx,
            )
            cb_t.grid(row=0, column=1, padx=0, pady=3, sticky="ew")
            self._mem_register_task_combo(cb_t)
            self._mem_bind_combo_capture(cb_t, lambda: self.var_tarefa_ctx.get(), "task")

            ctk.CTkLabel(self.frm_gatilho, text="Campo:").grid(
                row=1, column=0, padx=(0, 6), pady=3, sticky="w"
            )
            cb_c = ctk.CTkComboBox(
                self.frm_gatilho,
                values=self._mem_get_fields(),
                variable=self.var_campo,
            )
            cb_c.grid(row=1, column=1, padx=0, pady=3, sticky="ew")
            self._mem_register_field_combo(cb_c)
            self._mem_bind_combo_capture(cb_c, lambda: self.var_campo.get(), "field")

            ctk.CTkLabel(self.frm_gatilho, text="Resposta:").grid(
                row=2, column=0, padx=(0, 6), pady=3, sticky="w"
            )
            ent_r = ctk.CTkEntry(self.frm_gatilho, textvariable=self.var_resposta)
            ent_r.grid(row=2, column=1, padx=0, pady=3, sticky="ew")
            ent_r.bind("<Return>", lambda e: self._update_preview())
            ent_r.bind("<FocusOut>", lambda e: self._update_preview())
        elif t == "Concluída TAREFA":
            ctk.CTkLabel(self.frm_gatilho, text="Tarefa concluída:").grid(
                row=0, column=0, padx=(0, 6), pady=3, sticky="w"
            )
            cb_done = ctk.CTkComboBox(
                self.frm_gatilho,
                values=self._mem_get_tasks(),
                variable=self.var_tarefa_done,
            )
            cb_done.grid(row=0, column=1, padx=0, pady=3, sticky="ew")
            self._mem_register_task_combo(cb_done)
            self._mem_bind_combo_capture(cb_done, lambda: self.var_tarefa_done.get(), "task")
        else:
            ctk.CTkLabel(self.frm_gatilho, text="Evento:").grid(
                row=0, column=0, padx=(0, 6), pady=3, sticky="w"
            )
            ctk.CTkEntry(self.frm_gatilho, textvariable=self.var_evento).grid(
                row=0, column=1, padx=0, pady=3, sticky="ew"
            )
        self.after(0, self._update_preview)
        # REMOVIDO: ScrollFrame não é mais necessário
        # _restore_scroll(canvas, y, self)

    def _when_text(self: 'RNBuilder') -> str:
        lang = get_lang()
        t = self.var_gatilho_tipo.get()
        if t == GATILHOS[0]:
            return f"Sempre que inserido novo {CUR_L}{self.var_obj.get().strip()}{CUR_R}" if lang == 'pt' \
                   else f"Siempre que se inserte un nuevo {CUR_L}{self.var_obj.get().strip()}{CUR_R}"
        if t == GATILHOS[1]:
            if lang == 'es':
                return (f"En la conclusión de la tarea {CUR_L}{self.var_tarefa_ctx.get().strip()}{CUR_R}, "
                        f"si el campo {CUR_L}{self.var_campo.get().strip()}{CUR_R} "
                        f"es respondido con {CUR_L}{self.var_resposta.get().strip()}{CUR_R}")
            return (f"Na conclusão da tarefa {CUR_L}{self.var_tarefa_ctx.get().strip()}{CUR_R}, "
                    f"se o campo {CUR_L}{self.var_campo.get().strip()}{CUR_R} "
                    f"for respondido com {CUR_L}{self.var_resposta.get().strip()}{CUR_R}")
        if t == GATILHOS[2]:
            return f"Concluída a tarefa {CUR_L}{self.var_tarefa_done.get().strip()}{CUR_R}" if lang == 'pt' \
                   else f"Concluida la tarea {CUR_L}{self.var_tarefa_done.get().strip()}{CUR_R}"
        return f"Após {CUR_L}{self.var_evento.get().strip()}{CUR_R}" if lang == 'pt' \
               else f"Tras {CUR_L}{self.var_evento.get().strip()}{CUR_R}"

    def _cond_text(self: 'RNBuilder') -> str:
        texts = [r.to_text() for r in getattr(self, 'cond_rows', [])]
        texts = [t for t in texts if t]
        conj = getattr(self, 'var_conj', tk.StringVar(value='E')).get()
        return _join_conditions(texts, conj) if texts else ""

    def _acoes_text(self: 'RNBuilder', rows) -> str:
        parts = [r.to_text() for r in rows]
        parts = [p for p in parts if p]
        if not parts:
            return ""
        out = parts[0]
        # O conector "; e" funciona bem para ligar frases completas como "o status é atualizado..."
        for p in parts[1:]:
            out += f"; e {p}"
        return out

    # --- MELHORIA UX: Função de reordenar ---
    def _move_row(self: 'RNBuilder', widget, delta, row_list, frame_parent):
        try:
            idx = row_list.index(widget)
        except ValueError:
            return # Widget não está na lista, abortar

        new_idx = idx + delta
        if not (0 <= new_idx < len(row_list)):
            return # Fora dos limites

        # Reordena a lista
        row_list[idx], row_list[new_idx] = row_list[new_idx], row_list[idx]

        # Re-renderiza a UI (forma mais segura)
        if row_list and isinstance(row_list[0], LinhaCondicao):
            self._relayout_cond_rows()
        else:
            self._relayout_acao_rows()

        self._update_preview()

    # _update_preview foi movido para a PARTE 6 para centralizar a atualização da prévia

    RNBuilder._build_rule = _build_rule
    RNBuilder._reset_builder_defaults = _reset_builder_defaults
    RNBuilder._destroy_rows = _destroy_rows
    RNBuilder._relayout_cond_rows = _relayout_cond_rows
    RNBuilder._relayout_acao_rows = _relayout_acao_rows
    RNBuilder._ensure_min_builder_rows = _ensure_min_builder_rows
    RNBuilder._clear_conditions = _clear_conditions
    RNBuilder._clear_actions = _clear_actions
    RNBuilder._add_cond = _add_cond
    RNBuilder._add_acao = _add_acao
    RNBuilder._insert_frequent_flow = _insert_frequent_flow
    RNBuilder._insert_frequent_return = _insert_frequent_return
    RNBuilder._insert_frequent_condition = _insert_frequent_condition
    # RNBuilder._insert_frequent_close = _insert_frequent_close # Removida
    RNBuilder._refresh_gatilho_fields = _refresh_gatilho_fields
    RNBuilder._when_text = _when_text
    RNBuilder._cond_text = _cond_text
    RNBuilder._acoes_text = _acoes_text
    RNBuilder._move_row = _move_row # Adicionada
    # RNBuilder._update_preview = _update_preview # Removida (movida para PARTE 6)

_attach_builder_to_RNBuilder()


# ==============================================
#  PARTE 6/6 — Painéis finais (prévia + RNs)
# ==============================================

def _attach_panels_to_RNBuilder():
    def _build_panels(self: 'RNBuilder'):
        parent = getattr(self, "content", self)
        container = ctk.CTkFrame(parent)
        container.grid(row=0, column=0, sticky="nsew", padx=(10, 6), pady=6)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=4)
        container.grid_rowconfigure(1, weight=5)

        preview_group = group(
            container,
            "Pré-visualização da RN atual",
            row=0,
            col=0,
            padx=(0, 0),
            pady=(0, 8),
            sticky="nsew",
        )
        preview_group.grid_rowconfigure(1, weight=1)

        left_btnbar = ctk.CTkFrame(preview_group, fg_color="transparent")
        left_btnbar.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 6))
        ctk.CTkButton(left_btnbar, text="Adicionar RN", command=self._add_rn, width=160).pack(side="left", padx=(0, 6))
        ctk.CTkButton(left_btnbar, text="Adicionar RN e preparar oposto (Sim/Não)",
                      command=self._add_rn_and_prepare_opposite, width=300).pack(side="left", padx=(0, 6))
        ctk.CTkButton(left_btnbar, text="Limpar pré-visualização", command=self._clear_preview, width=200).pack(side="left")

        self.prev_box = SafeCTkTextbox(preview_group, height=200)
        self.prev_box.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        try:
            self.prev_box.configure(wrap="word")
        except Exception:
            pass

        rn_group = group(
            container,
            "RNs (lista final)",
            row=1,
            col=0,
            padx=(0, 0),
            pady=(0, 0),
            sticky="nsew",
        )
        rn_group.grid_rowconfigure(1, weight=1)
        rn_group.grid_rowconfigure(2, weight=1)

        right_btnbar = ctk.CTkFrame(rn_group, fg_color="transparent")
        right_btnbar.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 6))
        ctk.CTkButton(right_btnbar, text="Copiar RN", command=self._copy_single_rn, width=120).pack(side="left", padx=(0, 6))
        ctk.CTkButton(right_btnbar, text="Copiar tudo", command=self._copy_all, width=110).pack(side="left", padx=(0, 6))
        ctk.CTkButton(right_btnbar, text="Salvar .txt", command=self._save_txt, width=110).pack(side="left", padx=(0, 6))
        ctk.CTkButton(right_btnbar, text="Limpar RNs", command=lambda: self._clear_rns(confirm=True), width=110).pack(side="left")

        self.rn_mgr = ctk.CTkScrollableFrame(rn_group, height=220)
        self.rn_mgr.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 6))
        self.rn_mgr.grid_columnconfigure(0, weight=1)

        self.txt = ctk.CTkTextbox(rn_group, height=200)
        self.txt.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        try:
            self.txt.configure(wrap="word")
        except Exception:
            pass

    # util dos painéis
    def _set_preview_text(self: 'RNBuilder', txt: str):
        # Esta função é mantida para compatibilidade, mas _clear_preview foi refatorada
        try:
            self.prev_box.configure(state="normal")
            self.prev_box.delete("1.0", "end")
            self.prev_box.insert("1.0", txt)
            self.prev_box.configure(state="disabled")
        except Exception:
            pass

    def _clear_preview(self: 'RNBuilder'):
        # Limpa o texto da pré-visualização
        try:
            self.prev_box.configure(state="normal")
            self.prev_box.delete("1.0", "end")
            self.prev_box.configure(state="disabled")
        except Exception:
            pass

    def _truncate(self: 'RNBuilder', s: str, n: int = 100) -> str:
        s = (s or "").replace("\n", " ").strip()
        return s if len(s) <= n else s[: n - 1] + "…"

    def _rebuild_rn_manager(self: 'RNBuilder'):
        for w in self.rn_mgr.winfo_children():
            w.destroy()
        for i, rn in enumerate(self.rns):
            row = ctk.CTkFrame(self.rn_mgr)
            row.grid(row=i, column=0, sticky="we", padx=4, pady=2)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(row, text=self._truncate(rn), anchor="w").grid(row=0, column=0, sticky="w", padx=(4, 6))
            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.grid(row=0, column=1, sticky="e")
            up = ctk.CTkButton(btns, text="↑", width=28, command=lambda idx=i: self._move_rn(idx, -1))
            down = ctk.CTkButton(btns, text="↓", width=28, command=lambda idx=i: self._move_rn(idx, +1))
            edit = ctk.CTkButton(btns, text="Editar", width=70, command=lambda idx=i: self._edit_rn(idx))
            delete = ctk.CTkButton(btns, text="Excluir", width=70, command=lambda idx=i: self._delete_rn(idx))
            up.pack(side="left", padx=(0, 4))
            down.pack(side="left", padx=(0, 8))
            edit.pack(side="left", padx=(0, 6))
            delete.pack(side="left")
            if i == 0:
                up.configure(state="disabled")
            if i == len(self.rns) - 1:
                down.configure(state="disabled")

    def _refresh_textbox(self: 'RNBuilder'):
        header_parts: list[str] = []
        try:
            header_parts.append(f"RN inicial: {int(self.start_idx.get())}")
        except Exception:
            pass
        preset = self.var_resp_preset.get()
        if preset == "Texto livre…":
            livre = self.var_resp_preset_free.get().strip()
            if livre:
                header_parts.append(f"Responsável padrão: {livre}")
        elif preset:
            header_parts.append(f"Responsável padrão: {preset}")
        header = " | ".join(header_parts)
        content = (header + "\n\n" if header else "") + "\n\n".join(self.rns)
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", content)
        self.txt.configure(state="disabled")
        self._rebuild_rn_manager()

    def _copy_all(self: 'RNBuilder'):
        txt = self.txt.get("1.0", "end").strip()
        if not txt:
            messagebox.showinfo("Nada para copiar", "Adicione ao menos uma RN.")
            return
        self.clipboard_clear()
        self.clipboard_append(txt)
        messagebox.showinfo("Copiado", "Todas as RNs foram copiadas.")

    def _copy_single_rn(self: 'RNBuilder'):
        try:
            sel = self.txt.get("sel.first", "sel.last").strip()
        except Exception:
            sel = ""
        if sel:
            payload = sel
        elif self.rns:
            payload = self.rns[-1]
        else:
            payload = self.prev_box.get("1.0", "end").strip()
        if payload:
            self.clipboard_clear()
            self.clipboard_append(payload)
            messagebox.showinfo("Copiado", "RN copiada para a área de transferência.")
        else:
            messagebox.showinfo("Nada para copiar", "Não há RN para copiar.")

    def _save_txt(self: 'RNBuilder'):
        txt = self.txt.get("1.0", "end").strip()
        if not txt:
            messagebox.showinfo("Nada para salvar", "Adicione ao menos uma RN.")
            return
        path = filedialog.asksaveasfilename(
            title="Salvar RNs",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile="rns_geradas.txt",
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(txt)
                messagebox.showinfo("Salvo", f"Arquivo salvo em:\n{path}")
            except Exception as e:
                messagebox.showerror("Erro ao salvar", str(e))

    def _move_rn(self: 'RNBuilder', idx: int, delta: int):
        j = idx + delta
        if 0 <= idx < len(self.rns) and 0 <= j < len(self.rns):
            self.rns[idx], self.rns[j] = self.rns[j], self.rns[idx]
            self._refresh_textbox()

    def _edit_rn(self: 'RNBuilder', idx: int):
        if not (0 <= idx < len(self.rns)):
            return
        top = ctk.CTkToplevel(self)
        top.title(f"Editar RN #{idx + 1}")
        top.geometry("740x420")
        box = ctk.CTkTextbox(top)
        box.pack(expand=True, fill="both", padx=10, pady=10)
        box.insert("1.0", self.rns[idx])
        btnbar = ctk.CTkFrame(top, fg_color="transparent")
        btnbar.pack(fill="x", padx=10, pady=(0, 10))

        def _save():
            txt = box.get("1.0", "end").strip()
            if txt:
                self.rns[idx] = txt
                self._refresh_textbox()
            top.destroy()

        ctk.CTkButton(btnbar, text="Salvar", command=_save, width=120).pack(side="right")
        ctk.CTkButton(btnbar, text="Cancelar", command=top.destroy, width=120).pack(side="right", padx=(0, 8))

    def _delete_rn(self: 'RNBuilder', idx: int):
        if not (0 <= idx < len(self.rns)):
            return
        if messagebox.askyesno("Excluir RN", f"Remover a RN #{idx + 1}?"):
            del self.rns[idx]
            self._refresh_textbox()

    def _update_preview(self: 'RNBuilder'):
        try:
            # Funções de texto da PARTE 5
            when = self._when_text()
            cond  = self._cond_text()
            acoes = self._acoes_text(getattr(self, 'acao_rows', []))

            # Referência ao prev_box da PARTE 6
            self.prev_box.configure(state="normal")
            self.prev_box.delete("1.0", "end")

            preview = when or ""

            if cond:
                link = " e " if (" se " in when or " Se " in when) else ", se "
                preview += (link if preview else "") + cond

            if acoes:
                preview += (", " if preview else "") + acoes

            if preview:
                preview += "."

            if not preview:
                preview = ""

            self.prev_box.insert("end", preview)

        except Exception as e:
            # Firewall
            try:
                self.prev_box.delete("1.0", "end")
                self.prev_box.insert("end", f"Erro no preview: {e}")
            except Exception:
                pass # Falha total
        finally:
            try:
                self.prev_box.configure(state="disabled")
            except Exception:
                pass # O widget pode não existir ainda

    def _add_rn(self: 'RNBuilder'):
        when = self._when_text()
        cond = self._cond_text()
        acoes = self._acoes_text(getattr(self, 'acao_rows', []))
        if not acoes:
            messagebox.showwarning("Faltam ações", "Adicione pelo menos uma ação.")
            return
        idx = int(self.start_idx.get()) + len(self.rns)
        rn = _compose_rn(idx, when, cond, acoes)
        self.rns.append(rn)
        self._refresh_textbox()

    def _add_rn_and_prepare_opposite(self: 'RNBuilder'):
        self._add_rn()
        try:
            if self.var_gatilho_tipo.get() == 'Em TAREFA se CAMPO for RESPOSTA':
                lang = get_lang()
                resp = (self.var_resposta.get() or '').strip().lower()
                def _norm_es(x: str) -> str:
                    return x.replace('í', 'i').replace('Í', 'i')
                if lang == 'es':
                    r = _norm_es(resp)
                    if r == 'si':
                        self.var_resposta.set('No')
                    elif r == 'no':
                        self.var_resposta.set('Sí')
                else:
                    if resp == 'sim':
                        self.var_resposta.set('Não')
                    elif resp in ('não', 'nao'):
                        self.var_resposta.set('Sim')
        except Exception:
            pass
        self._destroy_rows(getattr(self, 'acao_rows', []))
        if hasattr(self, '_ensure_min_builder_rows'):
            self._ensure_min_builder_rows()
        self._update_preview()

    def _clear_rns(self: 'RNBuilder', *, confirm=True):
        if (not confirm) or messagebox.askyesno("Limpar", "Remover todas as RNs?"):
            self.rns.clear()
            self._refresh_textbox()

    RNBuilder._build_panels = _build_panels
    RNBuilder._set_preview_text = _set_preview_text
    RNBuilder._clear_preview = _clear_preview
    RNBuilder._truncate = _truncate
    RNBuilder._rebuild_rn_manager = _rebuild_rn_manager
    RNBuilder._refresh_textbox = _refresh_textbox
    RNBuilder._copy_all = _copy_all
    RNBuilder._copy_single_rn = _copy_single_rn
    RNBuilder._save_txt = _save_txt
    RNBuilder._move_rn = _move_rn
    RNBuilder._edit_rn = _edit_rn
    RNBuilder._delete_rn = _delete_rn
    RNBuilder._update_preview = _update_preview
    RNBuilder._add_rn = _add_rn
    RNBuilder._add_rn_and_prepare_opposite = _add_rn_and_prepare_opposite
    RNBuilder._clear_rns = _clear_rns

_attach_panels_to_RNBuilder()


# ===============
#  ENTRADA MAIN
# ===============
if __name__ == "__main__":
    try:
        app = RNBuilder()
        if not hasattr(app, 'builder_container'):
            app._build_rule()
        if not hasattr(app, 'prev_box'):
            app._build_panels()
        app.mainloop()
    except Exception as e:
        try:
            _show_fatal_error(e)
        finally:
            try:
                input("Pressione ENTER para sair...")
            except Exception:
                pass
