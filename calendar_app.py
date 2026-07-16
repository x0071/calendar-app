import sys, os, json, traceback
from datetime import datetime
if sys.platform == 'win32': import winreg

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QColorDialog,
                             QSlider, QCheckBox, QDialog, QLineEdit, QToolButton,
                             QTimeEdit, QMessageBox, QFrame, QListWidget, QListWidgetItem,
                             QMenu, QAction, QGroupBox, QAbstractItemView,
                             QSizePolicy, QSystemTrayIcon)
from PyQt5.QtGui import (QColor, QIcon, QPainter, QPen, QPainterPath,
                         QTransform, QRegion)
from PyQt5.QtCore import Qt, QDate, QSettings, QTime, QTimer, QEvent, QRectF, QPointF
import lunardate


class HolidayManager:
    holidays = {
        "2024": {"01-01":"元旦","02-10":"除夕","02-11":"春节","02-12":"春节","02-13":"春节","02-14":"春节","02-15":"春节","02-16":"春节","04-04":"清明节","04-05":"清明节","04-06":"清明节","05-01":"劳动节","05-02":"劳动节","05-03":"劳动节","06-10":"端午节","06-11":"端午节","06-12":"端午节","09-15":"中秋节","09-16":"中秋节","09-17":"中秋节","10-01":"国庆节","10-02":"国庆节","10-03":"国庆节","10-04":"国庆节","10-05":"国庆节","10-06":"国庆节","10-07":"国庆节"},
        "2025": {"01-01":"元旦","01-28":"除夕","01-29":"春节","01-30":"春节","01-31":"春节","02-01":"春节","02-02":"春节","02-03":"春节","04-04":"清明节","04-05":"清明节","04-06":"清明节","05-01":"劳动节","05-02":"劳动节","05-03":"劳动节","05-31":"端午节","06-01":"端午节","06-02":"端午节","10-06":"中秋节","10-07":"中秋节","10-08":"中秋节","10-01":"国庆节","10-02":"国庆节","10-03":"国庆节","10-04":"国庆节","10-05":"国庆节","10-06":"国庆节","10-07":"国庆节"},
        "2026": {"01-01":"元旦","02-16":"除夕","02-17":"春节","02-18":"春节","02-19":"春节","02-20":"春节","02-21":"春节","02-22":"春节","04-04":"清明节","04-05":"清明节","04-06":"清明节","05-01":"劳动节","05-02":"劳动节","05-03":"劳动节","06-20":"端午节","06-21":"端午节","06-22":"端午节","09-25":"中秋节","09-26":"中秋节","09-27":"中秋节","10-01":"国庆节","10-02":"国庆节","10-03":"国庆节","10-04":"国庆节","10-05":"国庆节","10-06":"国庆节","10-07":"国庆节"},
        "2027": {"01-01":"元旦","02-05":"除夕","02-06":"春节","02-07":"春节","02-08":"春节","02-09":"春节","02-10":"春节","02-11":"春节","04-04":"清明节","04-05":"清明节","04-06":"清明节","05-01":"劳动节","05-02":"劳动节","05-03":"劳动节","06-10":"端午节","06-11":"端午节","06-12":"端午节","10-14":"中秋节","10-15":"中秋节","10-16":"中秋节","10-01":"国庆节","10-02":"国庆节","10-03":"国庆节","10-04":"国庆节","10-05":"国庆节","10-06":"国庆节","10-07":"国庆节"},
        "2028": {"01-01":"元旦","01-24":"除夕","01-25":"春节","01-26":"春节","01-27":"春节","01-28":"春节","01-29":"春节","01-30":"春节","04-04":"清明节","04-05":"清明节","04-06":"清明节","05-01":"劳动节","05-02":"劳动节","05-03":"劳动节","05-30":"端午节","05-31":"端午节","06-01":"端午节","09-24":"中秋节","09-25":"中秋节","09-26":"中秋节","10-01":"国庆节","10-02":"国庆节","10-03":"国庆节","10-04":"国庆节","10-05":"国庆节","10-06":"国庆节","10-07":"国庆节"},
    }

    @staticmethod
    def get_holiday(year, month, day):
        dk = f"{month:02d}-{day:02d}"
        return HolidayManager.holidays.get(str(year), {}).get(dk, "")


class LunarCalendar:
    LUNAR_MONTHS = ["","正月","二月","三月","四月","五月","六月","七月","八月","九月","十月","冬月","腊月"]
    LUNAR_DAYS = ["","初一","初二","初三","初四","初五","初六","初七","初八","初九","初十","十一","十二","十三","十四","十五","十六","十七","十八","十九","二十","廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十"]
    SOLAR_TERMS = {
        2024: {"01-06":"小寒","01-20":"大寒","02-04":"立春","02-19":"雨水","03-05":"惊蛰","03-20":"春分","04-04":"清明","04-19":"谷雨","05-05":"立夏","05-20":"小满","06-05":"芒种","06-21":"夏至","07-06":"小暑","07-22":"大暑","08-07":"立秋","08-22":"处暑","09-07":"白露","09-22":"秋分","10-08":"寒露","10-23":"霜降","11-07":"立冬","11-22":"小雪","12-06":"大雪","12-21":"冬至"},
        2025: {"01-05":"小寒","01-20":"大寒","02-03":"立春","02-18":"雨水","03-05":"惊蛰","03-20":"春分","04-04":"清明","04-20":"谷雨","05-05":"立夏","05-21":"小满","06-05":"芒种","06-21":"夏至","07-07":"小暑","07-22":"大暑","08-07":"立秋","08-23":"处暑","09-07":"白露","09-23":"秋分","10-08":"寒露","10-23":"霜降","11-07":"立冬","11-22":"小雪","12-07":"大雪","12-21":"冬至"},
        2026: {"01-05":"小寒","01-20":"大寒","02-03":"立春","02-18":"雨水","03-05":"惊蛰","03-20":"春分","04-04":"清明","04-20":"谷雨","05-05":"立夏","05-21":"小满","06-05":"芒种","06-21":"夏至","07-07":"小暑","07-22":"大暑","08-07":"立秋","08-23":"处暑","09-07":"白露","09-23":"秋分","10-08":"寒露","10-23":"霜降","11-07":"立冬","11-22":"小雪","12-07":"大雪","12-22":"冬至"},
        2027: {"01-05":"小寒","01-20":"大寒","02-04":"立春","02-18":"雨水","03-05":"惊蛰","03-20":"春分","04-04":"清明","04-20":"谷雨","05-05":"立夏","05-21":"小满","06-05":"芒种","06-21":"夏至","07-07":"小暑","07-22":"大暑","08-07":"立秋","08-23":"处暑","09-07":"白露","09-23":"秋分","10-08":"寒露","10-23":"霜降","11-07":"立冬","11-22":"小雪","12-07":"大雪","12-22":"冬至"},
        2028: {"01-05":"小寒","01-20":"大寒","02-04":"立春","02-19":"雨水","03-05":"惊蛰","03-20":"春分","04-04":"清明","04-19":"谷雨","05-05":"立夏","05-20":"小满","06-05":"芒种","06-21":"夏至","07-06":"小暑","07-22":"大暑","08-07":"立秋","08-22":"处暑","09-07":"白露","09-22":"秋分","10-08":"寒露","10-23":"霜降","11-07":"立冬","11-22":"小雪","12-06":"大雪","12-21":"冬至"},
        2029: {"01-05":"小寒","01-20":"大寒","02-03":"立春","02-18":"雨水","03-05":"惊蛰","03-20":"春分","04-04":"清明","04-20":"谷雨","05-05":"立夏","05-21":"小满","06-05":"芒种","06-21":"夏至","07-07":"小暑","07-22":"大暑","08-07":"立秋","08-23":"处暑","09-07":"白露","09-23":"秋分","10-08":"寒露","10-23":"霜降","11-07":"立冬","11-22":"小雪","12-07":"大雪","12-21":"冬至"},
        2030: {"01-05":"小寒","01-20":"大寒","02-03":"立春","02-18":"雨水","03-05":"惊蛰","03-20":"春分","04-04":"清明","04-20":"谷雨","05-05":"立夏","05-21":"小满","06-05":"芒种","06-21":"夏至","07-07":"小暑","07-22":"大暑","08-07":"立秋","08-23":"处暑","09-07":"白露","09-23":"秋分","10-08":"寒露","10-23":"霜降","11-07":"立冬","11-22":"小雪","12-07":"大雪","12-22":"冬至"},
    }
    @staticmethod
    def get_lunar_date(year, month, day):
        try:
            l = lunardate.LunarDate.from_solar_date(year, month, day)
            m = l.month; d = l.day
            mn = LunarCalendar.LUNAR_MONTHS[m] if m <= 12 else f"闰{LunarCalendar.LUNAR_MONTHS[m-12]}"
            if l.is_leap_month: mn = f"闰{LunarCalendar.LUNAR_MONTHS[m]}"
            return f"{mn}{LunarCalendar.LUNAR_DAYS[d]}" if d<=30 else ""
        except: return ""
    @staticmethod
    def get_solar_term(year, month, day):
        return LunarCalendar.SOLAR_TERMS.get(year, {}).get(f"{month:02d}-{day:02d}", "")


class CustomCalendarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        today = QDate.currentDate()
        self.year = today.year()
        self.month = today.month()
        self.selected_date = today
        self.hover_date = None
        self.setMouseTracking(True)
        self.weekday_names = ["一","二","三","四","五","六","日"]
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def date_from_pos(self, pos):
        if self.width()<7 or self.height()<40: return None
        cw = self.width()/7.0
        wh = max(24, self.height()*0.10)
        rh = (self.height()-wh)/6.0
        if pos.y()<wh: return None
        col = int(pos.x()/cw); row = int((pos.y()-wh)/rh)
        if not (0<=col<=6 and 0<=row<=5): return None
        fd = QDate(self.year, self.month, 1)
        d = row*7+col - (fd.dayOfWeek()-1)+1
        if 1<=d<=fd.daysInMonth(): return QDate(self.year, self.month, d)
        return None

    def prev_month(self):
        d = QDate(self.year, self.month, 1).addMonths(-1); self.year, self.month = d.year(), d.month(); self.update()
    def next_month(self):
        d = QDate(self.year, self.month, 1).addMonths(1); self.year, self.month = d.year(), d.month(); self.update()
    def get_current_title(self): return f"{self.year}年 {self.month}月"

    def get_tasks_for_date(self, year, month, day):
        return self.parent_app.tasks.get(f"{year:04d}-{month:02d}-{day:02d}", []) if self.parent_app else []

    def paintEvent(self, event):
        if self.width()<7 or self.height()<40: return
        p = QPainter(self)
        try: self._paint(p)
        except Exception as e:
            p.setPen(QColor(255,0,0)); p.drawText(self.rect(), Qt.AlignCenter, f"Paint error: {e}")
        finally: p.end()

    def _paint(self, p):
        app = self.parent_app
        if app and hasattr(app, 'bg_color'):
            r,g,b,a = app.bg_color.red(), app.bg_color.green(), app.bg_color.blue(), int(app.bg_transparency*2.55)
            bg = QColor(r,g,b,a)
        else: bg = QColor(80, 130, 180, 153)
        tc, wc = QColor(255,255,255,230), QColor(255,180,130,230)
        dc, tdc, sc = QColor(200,200,200,80), QColor(120,200,255,180), QColor(100,180,255,220)
        p.fillRect(self.rect(), bg)
        w,h = self.width(), self.height()
        cw, wh = w/7.0, max(26, int(h*0.09))
        dh = (h-wh)/6.0
        if dh<10: return
        f = p.font(); f.setPointSize(max(9,int(wh*0.32))); f.setBold(True); p.setFont(f)
        for i,n in enumerate(self.weekday_names):
            p.setPen(wc if i>=5 else tc)
            p.drawText(QRectF(i*cw, 0, cw, wh), Qt.AlignCenter, n)
        fd = QDate(self.year, self.month, 1)
        so, dim = fd.dayOfWeek()-1, fd.daysInMonth()
        pm = fd.addMonths(-1); pd = pm.daysInMonth()
        nm = fd.addMonths(1); td = QDate.currentDate()
        for row in range(6):
            for col in range(7):
                di = row*7+col; dn = di-so+1
                x = int(col*cw); y = int(wh+row*dh)
                cr = QRectF(x, y, cw, dh)
                if dn<1: d,qd = pd+dn, QDate(pm.year(),pm.month(),pd+dn)
                elif dn>dim: d,qd = dn-dim, QDate(nm.year(),nm.month(),dn-dim)
                else: d,qd = dn, QDate(self.year, self.month, dn)
                ic = qd.month()==self.month and qd.year()==self.year
                it, ise = qd==td, qd==self.selected_date
                iw = qd.dayOfWeek()>=6
                if ise and ic: p.fillRect(cr.adjusted(4,4,-4,-4), sc)
                elif it and ic: p.fillRect(cr.adjusted(4,4,-4,-4), tdc)
                color = QColor(255,255,255) if (it or (ise and ic)) else (dc if not ic else (wc if iw else tc))
                f.setPointSize(max(9,int(dh*0.28))); f.setBold(True); p.setFont(f); p.setPen(color)
                nr = QRectF(x, y+2, cw, dh*0.5); p.drawText(nr, Qt.AlignTop|Qt.AlignHCenter, str(d))
                lu = LunarCalendar.get_lunar_date(qd.year(),qd.month(),qd.day())
                st = LunarCalendar.get_solar_term(qd.year(),qd.month(),qd.day())
                ho = HolidayManager.get_holiday(qd.year(),qd.month(),qd.day())
                lb, lc = "", QColor(200,200,200,180)
                if ho: lb, lc = ho[:2], QColor(255,100,100,230)
                elif st: lb, lc = st[:2], QColor(100,200,100,220)
                elif lu and len(lu)>=2:
                    try:
                        lo = lunardate.LunarDate.from_solar_date(qd.year(),qd.month(),qd.day())
                        lb = lu[:-2] if lo.day==1 else lu[-2:]
                    except: lb = lu[-2:]
                if lb and ic:
                    f.setPointSize(max(6,int(dh*0.15))); f.setBold(False); p.setFont(f); p.setPen(lc)
                    p.drawText(QRectF(x, y+dh*0.55, cw, dh*0.35), Qt.AlignCenter, lb)
                ts = self.get_tasks_for_date(qd.year(),qd.month(),qd.day())
                if ts and ic:
                    n = min(len(ts),3); dr = max(2,int(cw*0.03)); sp = dr*3
                    sx = cr.center().x()-(n-1)*sp/2; dy = cr.bottom()-dr*2
                    p.setBrush(QColor(255,200,50,230)); p.setPen(Qt.NoPen)
                    for i in range(n): p.drawEllipse(QPointF(sx+i*sp, dy), dr, dr)

    def mousePressEvent(self, e):
        if e.button()==Qt.LeftButton:
            d = self.date_from_pos(e.pos())
            if d: self.selected_date=d; self.update()
            if d and self.parent_app: self.parent_app.on_date_clicked(d)

    def mouseMoveEvent(self, e):
        d = self.date_from_pos(e.pos())
        if d!=self.hover_date: self.hover_date=d; self.setCursor(Qt.PointingHandCursor if d else Qt.ArrowCursor)

    def contextMenuEvent(self, e):
        d = self.date_from_pos(e.pos())
        if not d: return
        dk = f"{d.year():04d}-{d.month():02d}-{d.day():02d}"
        ts = self.parent_app.tasks.get(dk,[])
        m = QMenu(self)
        m.setStyleSheet("QMenu{background-color:rgba(50,60,80,240);color:white;border:1px solid rgba(255,255,255,30);}QMenu::item{padding:6px 25px;}QMenu::item:selected{background-color:rgba(100,180,255,150);}QMenu::separator{background:rgba(255,255,255,20);height:1px;margin:4px 10px;}")
        a = m.addAction(f"+ 为 {d.month()}月{d.day()}日 添加任务")
        a.triggered.connect(lambda dd=d: QTimer.singleShot(0,lambda:self.parent_app.on_date_double_clicked(dd)))
        if ts:
            m.addSeparator()
            for i,t in enumerate(ts):
                ti = t.get('title','无标题'); ts2 = t.get('time','')
                di = f"{ts2} {ti}" if ts2 else ti
                ac = m.addAction(f"📋 {di}")
                ac.triggered.connect(lambda dd=d,idx=i: QTimer.singleShot(0,lambda:self.parent_app.edit_task(dd,idx)))
            m.addSeparator()
            da = m.addAction("🗑 删除此日期所有任务")
            da.triggered.connect(lambda dd=d: QTimer.singleShot(0,lambda:self.parent_app.delete_date_tasks(dd)))
        m.exec_(e.globalPos())


class TaskDialog(QDialog):
    def __init__(self, parent, date, edit_task=None, task_index=None):
        super().__init__(parent)
        self.date=date; self.edit_task=edit_task; self.task_index=task_index
        ise = edit_task is not None
        self.setWindowTitle(f"{date.year()}年{date.month()}月{date.day()}日 - {'编辑' if ise else '添加'}任务")
        self.setFixedSize(320,300)
        self.setStyleSheet("QDialog{background-color:rgba(80,120,160,235);}QLabel{color:white;}QLineEdit,QTextEdit,QTimeEdit{background-color:rgba(255,255,255,30);border:1px solid rgba(255,255,255,40);color:white;border-radius:4px;padding:4px;}QPushButton{background-color:rgba(100,180,255,150);border:none;color:white;padding:6px 18px;border-radius:4px;}QPushButton:hover{background-color:rgba(100,180,255,210);}")
        lo = QVBoxLayout()
        self.ti = QLineEdit(); self.ti.setPlaceholderText("任务标题")
        if ise and edit_task.get('title'): self.ti.setText(edit_task['title'])
        lo.addWidget(QLabel("任务标题：")); lo.addWidget(self.ti)
        tl = QHBoxLayout()
        self.te = QTimeEdit(QTime.currentTime()); self.te.setDisplayFormat("HH:mm")
        if ise and edit_task.get('time'):
            t = QTime.fromString(edit_task['time'],"HH:mm")
            if t.isValid(): self.te.setTime(t)
        tl.addWidget(QLabel("提醒时间：")); tl.addWidget(self.te); tl.addStretch()
        lo.addLayout(tl)
        self.ci = QTextEdit(); self.ci.setPlaceholderText("任务内容..."); self.ci.setFixedHeight(80)
        if ise and edit_task.get('content'): self.ci.setPlainText(edit_task['content'])
        lo.addWidget(QLabel("任务内容：")); lo.addWidget(self.ci); lo.addStretch()
        bl = QHBoxLayout()
        self.ok = QPushButton("确定"); self.cancel = QPushButton("取消")
        bl.addStretch(); bl.addWidget(self.ok); bl.addWidget(self.cancel)
        lo.addLayout(bl)
        self.setLayout(lo)
        self.ok.clicked.connect(self.accept); self.cancel.clicked.connect(self.reject)

    def get_task(self):
        return {"title":self.ti.text().strip(),"time":self.te.time().toString("HH:mm"),
                "content":self.ci.toPlainText().strip(),
                "date":f"{self.date.year()}-{self.date.month():02d}-{self.date.day():02d}"}


# ========== 新增：常驻提醒弹窗 ==========
class ReminderPopup(QDialog):
    """常驻提醒弹窗，需手动关闭，不会自动消失"""
    def __init__(self, title, content, time=""):
        super().__init__()
        # 无边框、窗口置顶、工具窗口（不在任务栏显示图标）
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(320, 130)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 12)
        main_layout.setSpacing(8)

        # 提醒标题
        title_label = QLabel("⏰ 任务提醒")
        title_label.setStyleSheet("color: rgb(255, 200, 100); font-size: 13px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # 任务标题（包含时间）
        display_title = f"{title} ({time})" if time else title
        task_title = QLabel(display_title)
        task_title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        task_title.setWordWrap(True)
        main_layout.addWidget(task_title)

        # 任务内容
        if content:
            content_label = QLabel(content)
            content_label.setStyleSheet("color: rgba(255,255,255,220); font-size: 12px;")
            content_label.setWordWrap(True)
            main_layout.addWidget(content_label)

        main_layout.addStretch(1)

        # 关闭按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("知道了")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(100, 180, 255, 150);
                border: none;
                color: white;
                padding: 5px 18px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(100, 180, 255, 210);
            }
        """)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        main_layout.addLayout(btn_layout)

    def paintEvent(self, event):
        """绘制圆角半透明背景"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(45, 65, 95, 245))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 10, 10)

    def show_at_bottom_right(self):
        """显示在屏幕右下角，避开任务栏"""
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 20
        self.move(x, y)
        self.show()
        self.raise_()
        self.activateWindow()
# ======================================


class TaskManagerDialog(QDialog):
    def __init__(self, parent, tasks):
        super().__init__(parent)
        self.parent_app=parent; self.tasks=tasks
        self.setWindowTitle("任务管理"); self.setMinimumSize(420,380)
        self.setStyleSheet("QDialog{background-color:rgba(50,60,80,240);}QLabel{color:white;}QLineEdit,QTextEdit,QTimeEdit{background-color:rgba(255,255,255,25);border:1px solid rgba(255,255,255,35);color:white;border-radius:4px;padding:3px;}QPushButton{background-color:rgba(100,180,255,150);border:none;color:white;padding:5px 14px;border-radius:4px;}QPushButton:hover{background-color:rgba(100,180,255,210);}QPushButton#db{background-color:rgba(255,100,100,150);}QPushButton#db:hover{background-color:rgba(255,100,100,210);}QListWidget{background-color:rgba(255,255,255,10);border:1px solid rgba(255,255,255,20);color:white;border-radius:6px;padding:4px;}QListWidget::item{padding:4px 8px;border-radius:3px;}QListWidget::item:selected{background-color:rgba(100,180,255,120);}QGroupBox{color:rgba(255,255,255,200);border:1px solid rgba(255,255,255,20);border-radius:6px;margin-top:10px;padding-top:14px;}QGroupBox::title{subcontrol-origin:margin;left:10px;padding:0 5px;}QScrollBar:vertical{background:rgba(255,255,255,8);width:8px;border-radius:4px;}QScrollBar::handle:vertical{background:rgba(255,255,255,25);border-radius:4px;min-height:30px;}")
        self.cs_date=None; self.cs_idx=None
        lo = QVBoxLayout(self)
        tl = QHBoxLayout()
        tl_label = QLabel("📅 所有任务计划"); tl_label.setStyleSheet("font-size:15px;font-weight:bold;"); tl.addWidget(tl_label)
        tl.addStretch()
        rb = QPushButton("刷新"); rb.clicked.connect(self.refresh_list); tl.addWidget(rb)
        da = QPushButton("删除全部"); da.setObjectName("db"); da.clicked.connect(self.delete_all); tl.addWidget(da)
        lo.addLayout(tl)
        self.list_w = QListWidget(); self.list_w.setSelectionMode(QAbstractItemView.SingleSelection)
        lo.addWidget(self.list_w)
        dg = QGroupBox("任务详情"); dl = QVBoxLayout(dg)
        dh = QHBoxLayout()
        self.dt = QLineEdit(); self.dt.setPlaceholderText("任务标题")
        dh.addWidget(QLabel("标题:")); dh.addWidget(self.dt)
        self.de = QTimeEdit(); self.de.setDisplayFormat("HH:mm")
        dh.addWidget(QLabel("时间:")); dh.addWidget(self.de)
        dl.addLayout(dh)
        self.dc = QTextEdit(); self.dc.setPlaceholderText("任务内容..."); self.dc.setFixedHeight(60)
        dl.addWidget(self.dc)
        bl = QHBoxLayout()
        sb = QPushButton("保存修改"); sb.clicked.connect(self.save_edit)
        db = QPushButton("删除此任务"); db.setObjectName("db"); db.clicked.connect(self.delete_sel)
        bl.addStretch(); bl.addWidget(sb); bl.addWidget(db)
        dl.addLayout(bl); lo.addWidget(dg)
        self.list_w.currentItemChanged.connect(self.on_select)
        self.refresh_list()

    def refresh_list(self):
        self.tasks=self.parent_app.tasks; self.list_w.clear()
        self.cs_date=None; self.cs_idx=None; self.dt.clear(); self.dc.clear()
        if not self.tasks: self.list_w.addItem("（暂无任务）"); return
        for dk in sorted(self.tasks):
            for idx,t in enumerate(self.tasks[dk]):
                ti=t.get('title','无标题'); ts2=t.get('time','')
                di = f"{dk} [{ts2}]  {ti}" if ts2 else f"{dk}  {ti}"
                it = QListWidgetItem(di); it.setData(Qt.UserRole,{'date':dk,'index':idx})
                self.list_w.addItem(it)

    def on_select(self, cur, prev):
        if not cur: return
        d = cur.data(Qt.UserRole)
        if not d: self.cs_date=None; self.cs_idx=None; return
        self.cs_date=d['date']; self.cs_idx=d['index']
        t = self.tasks.get(d['date'],[])[d['index']]
        self.dt.setText(t.get('title',''))
        tv = QTime.fromString(t.get('time','00:00'),"HH:mm")
        if tv.isValid(): self.de.setTime(tv)
        self.dc.setPlainText(t.get('content',''))

    def save_edit(self):
        if self.cs_date is None: QMessageBox.warning(self,"提示","请先选择一个任务"); return
        ti = self.dt.text().strip()
        if not ti: QMessageBox.warning(self,"提示","任务标题不能为空"); return
        self.parent_app.tasks[self.cs_date][self.cs_idx].update(title=ti,time=self.de.time().toString("HH:mm"),content=self.dc.toPlainText().strip(),reminded=False)
        self.parent_app.save_tasks(); self.refresh_list()
        self.parent_app.calendar.update(); QMessageBox.information(self,"成功","任务已更新")

    def delete_sel(self):
        if self.cs_date is None: QMessageBox.warning(self,"提示","请先选择一个任务"); return
        if QMessageBox.question(self,"确认删除","确定要删除此任务吗？",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            del self.parent_app.tasks[self.cs_date][self.cs_idx]
            if not self.parent_app.tasks[self.cs_date]: del self.parent_app.tasks[self.cs_date]
            self.parent_app.save_tasks(); self.refresh_list()
            self.parent_app.calendar.update()

    def delete_all(self):
        if not self.tasks: QMessageBox.warning(self,"提示","暂无任务可删除"); return
        if QMessageBox.question(self,"确认删除","确定要删除全部任务吗？此操作不可恢复！",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            self.parent_app.tasks.clear()
            self.parent_app.save_tasks(); self.refresh_list()
            self.parent_app.calendar.update()


class SettingsDialog(QDialog):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("设置"); self.setFixedSize(320, 290)
        self.setStyleSheet("QDialog{background-color:rgba(80,120,160,235);}QLabel{color:white;}QCheckBox{color:white;}QPushButton{background-color:rgba(100,180,255,150);border:none;color:white;padding:5px 15px;border-radius:4px;}QPushButton:hover{background-color:rgba(100,180,255,210);}QSlider::groove:horizontal{height:6px;background:rgba(255,255,255,30);border-radius:3px;}QSlider::handle:horizontal{background:rgba(100,180,255,200);width:16px;margin:-5px 0;border-radius:8px;}")
        lo = QVBoxLayout()
        cl = QHBoxLayout(); cl.addWidget(QLabel("背景颜色："))
        cb = QPushButton("选择"); cb.clicked.connect(self.choose_color)
        cl.addWidget(cb); lo.addLayout(cl)
        tl = QVBoxLayout()
        self.tl2 = QLabel(f"透明度: {self.app.bg_transparency}%")
        self.ts = QSlider(Qt.Horizontal); self.ts.setRange(0,100)
        self.ts.setValue(self.app.bg_transparency)
        self.ts.valueChanged.connect(self.update_trans)
        tl.addWidget(self.tl2); tl.addWidget(self.ts)
        lo.addLayout(tl)
        self.auto_cb = QCheckBox("开机自启")
        self.auto_cb.setChecked(self.app.auto_start)
        self.auto_cb.toggled.connect(self.app.toggle_auto_start)
        lo.addWidget(self.auto_cb)
        tm = QPushButton("📋 管理所有任务"); tm.clicked.connect(self.app.open_task_manager)
        lo.addWidget(tm); lo.addStretch()
        ok = QPushButton("确定"); ok.clicked.connect(self.accept)
        lo.addWidget(ok)
        self.setLayout(lo)

    def choose_color(self):
        c = QColorDialog.getColor(self.app.bg_color, self, "选择背景颜色")
        if c.isValid(): self.app.set_background_color(c)

    def update_trans(self, v):
        self.app.update_transparency(v); self.tl2.setText(f"透明度: {v}%")


class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("CalendarApp", "Calendar")
        self.tasks = self._load_tasks()
        self.bg_color = QColor(80, 130, 180)
        self.bg_transparency = 60
        self.auto_start = False
        self._reminder_popups = []  # 保持对提醒弹窗的引用，防止被垃圾回收
        self._init_ui()
        self._load_settings()
        self._init_tray()
        self._start_reminder()
        self._sync_autostart()

    def _init_ui(self):
        self.setWindowTitle("精美日历")
        self.setMinimumSize(200,200); self.resize(500,500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 双击检测
        self._click_timer = QTimer(); self._click_timer.setSingleShot(True)
        self._click_timer.setInterval(350)
        self._click_timer.timeout.connect(lambda: setattr(self, '_last_click_date', None))
        self._last_click_date = None
        # 图标
        ip = self._icon_path()
        if os.path.exists(ip): self.setWindowIcon(QIcon(ip))
        # 中央部件
        cw = QWidget(); cw.setAttribute(Qt.WA_NoSystemBackground,True); cw.setAutoFillBackground(False)
        self.setCentralWidget(cw)
        self.ml = QVBoxLayout(cw); self.ml.setContentsMargins(0,0,0,0)
        self.bf = QFrame(); self.bf.setObjectName("bg_frame"); self.bf.setMouseTracking(True)
        self.bl = QVBoxLayout(self.bf); self.bl.setContentsMargins(0,0,0,0); self.bl.setSpacing(0)
        # 导航栏
        nw = QWidget(); nw.setAttribute(Qt.WA_TranslucentBackground); nw.setMouseTracking(True)
        nl = QHBoxLayout(nw); nl.setContentsMargins(4,4,4,4); nl.setSpacing(4)
        bs = "QPushButton{background-color:rgba(255,255,255,15);color:rgba(255,255,255,210);border:none;border-radius:12px;font-size:12px;padding:0;}QPushButton:hover{background-color:rgba(100,160,220,80);}"
        pb = QPushButton("◀"); pb.setFixedSize(28,24); pb.setCursor(Qt.PointingHandCursor); pb.setStyleSheet(bs)
        pb.clicked.connect(self.prev_month); nl.addWidget(pb); nl.addStretch(1)
        self.myl = QLabel(); self.myl.setAlignment(Qt.AlignCenter)
        self.myl.setStyleSheet("QLabel{color:rgba(255,255,255,220);font-size:14px;font-weight:bold;}")
        nl.addWidget(self.myl); nl.addStretch(1)
        nb = QPushButton("▶"); nb.setFixedSize(28,24); nb.setCursor(Qt.PointingHandCursor); nb.setStyleSheet(bs)
        nb.clicked.connect(self.next_month); nl.addWidget(nb); nl.addSpacing(8)
        ts = "QToolButton{font-size:12px;background-color:rgba(120,200,120,150);border:none;color:white;border-radius:12px;padding:0;}QToolButton:hover{background-color:rgba(120,200,120,210);}"
        tb = QToolButton(); tb.setText("📋"); tb.setToolTip("管理所有任务"); tb.setFixedSize(26,24)
        tb.setCursor(Qt.PointingHandCursor); tb.setStyleSheet(ts)
        tb.clicked.connect(self.open_task_manager); nl.addWidget(tb)
        ss = "QToolButton{font-size:12px;background-color:rgba(100,180,255,150);border:none;color:white;border-radius:12px;padding:0;}QToolButton:hover{background-color:rgba(100,180,255,210);}"
        sb = QToolButton(); sb.setText("⚙"); sb.setToolTip("设置"); sb.setFixedSize(26,24)
        sb.setCursor(Qt.PointingHandCursor); sb.setStyleSheet(ss)
        sb.clicked.connect(self.open_settings); nl.addWidget(sb)
        xs = "QToolButton{font-size:12px;background-color:rgba(255,100,100,150);border:none;color:white;border-radius:12px;padding:0;}QToolButton:hover{background-color:rgba(255,100,100,210);}"
        cb = QToolButton(); cb.setText("✕"); cb.setToolTip("关闭"); cb.setFixedSize(26,24)
        cb.setCursor(Qt.PointingHandCursor); cb.setStyleSheet(xs)
        cb.clicked.connect(self._hide_to_tray); nl.addWidget(cb)
        self.bl.addWidget(nw)
        # 日历
        self.calendar = CustomCalendarWidget(self); self.calendar.setMouseTracking(True)
        self.bl.addWidget(self.calendar, 1)
        self.ml.addWidget(self.bf)
        self.set_background_color(self.bg_color)
        self.update_month_label()
        # 拖拽缩放状态
        self.dragging=False; self.resizing=False
        self.setMouseTracking(True)
        self.bf.installEventFilter(self); self.calendar.installEventFilter(self)
        self.nw = nw
        QApplication.instance().installEventFilter(self)

    def _init_tray(self):
        self.tray = QSystemTrayIcon(self)
        ip = self._icon_path()
        if os.path.exists(ip): self.tray.setIcon(QIcon(ip))
        self.tray.setToolTip("日历")
        m = QMenu()
        m.addAction("显示日历", self._show_from_tray)
        m.addSeparator()
        m.addAction("退出", self._quit)
        self.tray.setContextMenu(m)
        self.tray.activated.connect(lambda r: self._show_from_tray() if r==QSystemTrayIcon.Trigger else None)
        self.tray.show()

    def _hide_to_tray(self):
        self.hide()

    def _show_from_tray(self):
        self.show(); self.raise_(); self.activateWindow()

    def _quit(self):
        self._save_settings()
        self.tray.hide()
        QApplication.quit()

    def _icon_path(self):
        ip = os.path.join(os.path.dirname(os.path.abspath(__file__)), '001.ico')
        if not os.path.exists(ip):
            mp = getattr(sys, '_MEIPASS', None)
            if mp: ip = os.path.join(mp, '001.ico')
        return ip

    def eventFilter(self, obj, event):
        if event.type()==QEvent.MouseMove:
            if not self.resizing and not self.dragging:
                loc = self.mapFromGlobal(event.globalPos())
                self.setCursor(Qt.SizeFDiagCursor if (loc.x()>=self.width()-20 and loc.y()>=self.height()-20) else Qt.ArrowCursor)
            if self.resizing and event.buttons()==Qt.LeftButton:
                d = event.globalPos()-self.resize_start_pos
                self.resize(max(self.minimumWidth(),self.resize_start_size.width()+d.x()),
                           max(self.minimumHeight(),self.resize_start_size.height()+d.y()))
                return True
            if self.dragging and event.buttons()==Qt.LeftButton:
                self.move(event.globalPos()-self.drag_start_pos); return True
        if event.type()==QEvent.MouseButtonPress and event.button()==Qt.LeftButton:
            loc = self.mapFromGlobal(event.globalPos())
            if loc.x()>=self.width()-20 and loc.y()>=self.height()-20:
                self.resizing=True; self.resize_start_pos=event.globalPos()
                self.resize_start_size=self.size(); return True
            elif obj in (self.bf, self.nw):
                self.dragging=True
                self.drag_start_pos=event.globalPos()-self.frameGeometry().topLeft(); return True
        if event.type()==QEvent.MouseButtonRelease: self.dragging=False; self.resizing=False
        return super().eventFilter(obj, event)

    def update_month_label(self):
        self.myl.setText(self.calendar.get_current_title())

    def prev_month(self): self.calendar.prev_month(); self.update_month_label()
    def next_month(self): self.calendar.next_month(); self.update_month_label()

    def _start_reminder(self):
        self.rt = QTimer(); self.rt.timeout.connect(self._check_reminders); self.rt.start(30000)

    def _check_reminders(self):
        now = datetime.now()
        cd = now.strftime("%Y-%m-%d")
        ct = now.strftime("%H:%M")
        for t in self.tasks.get(cd, []):
            if t.get('time') == ct and not t.get('reminded', False):
                t['reminded'] = True
                self.save_tasks()
                popup = ReminderPopup(t['title'], t.get('content', ''), t.get('time', ''))
                popup.show_at_bottom_right()
                self._reminder_popups.append(popup)
                popup.finished.connect(lambda: self._cleanup_popup(popup))

    def _cleanup_popup(self, popup):
        if popup in self._reminder_popups:
            self._reminder_popups.remove(popup)

    def on_date_clicked(self, date):
        if (self._last_click_date is not None and
            date==self._last_click_date and self._click_timer.isActive()):
            self._click_timer.stop(); self._last_click_date=None
            self.on_date_double_clicked(date)
        else:
            self._last_click_date=date; self._click_timer.start()

    def on_date_double_clicked(self, date):
        d = TaskDialog(self, date)
        if d.exec_()==QDialog.Accepted:
            t = d.get_task()
            if t["title"]:
                dk = t["date"]
                self.tasks.setdefault(dk,[]).append(t)
                self.save_tasks()

    def edit_task(self, date, task_index):
        dk = f"{date.year():04d}-{date.month():02d}-{date.day():02d}"
        if dk in self.tasks and task_index<len(self.tasks[dk]):
            d = TaskDialog(self, date, edit_task=self.tasks[dk][task_index], task_index=task_index)
            if d.exec_()==QDialog.Accepted:
                t = d.get_task()
                if t["title"]: self.tasks[dk][task_index]=t; self.save_tasks()

    def delete_date_tasks(self, date):
        dk = f"{date.year():04d}-{date.month():02d}-{date.day():02d}"
        if dk in self.tasks:
            n = len(self.tasks[dk])
            if QMessageBox.question(self,"确认删除",f"确定要删除 {date.month()}月{date.day()}日 的全部 {n} 个任务吗？",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
                del self.tasks[dk]; self.save_tasks()

    def open_task_manager(self):
        TaskManagerDialog(self, self.tasks).exec_()

    def set_background_color(self, c):
        self.bg_color=c; self._update_bg()

    def update_transparency(self, v):
        self.bg_transparency=v; self._update_bg()

    def _update_bg(self):
        r,g,b = self.bg_color.red(),self.bg_color.green(),self.bg_color.blue()
        a = int(self.bg_transparency*2.55)
        self.bf.setStyleSheet(f"QFrame#bg_frame{{background-color:rgba({r},{g},{b},{a});border-radius:15px;}}")
        self.calendar.update(); self._update_mask()

    def _update_mask(self):
        try:
            path = QPainterPath(); path.addRoundedRect(self.rect().x(),self.rect().y(),self.rect().width(),self.rect().height(),15,15)
            self.setMask(QRegion(path.toFillPolygon(QTransform()).toPolygon()))
        except: pass

    def resizeEvent(self, e): super().resizeEvent(e); self._update_mask()
    def showEvent(self, e): super().showEvent(e); self._update_mask()

    def toggle_auto_start(self, checked):
        self.auto_start = checked
        self.settings.setValue("auto_start", checked)
        self._write_run_key(checked)

    def _write_run_key(self, checked):
        if sys.platform != 'win32': return
        try:
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r'Software\Microsoft\Windows\CurrentVersion\Run',
                               0, winreg.KEY_SET_VALUE)
            if checked:
                winreg.SetValueEx(k, '日历', 0, winreg.REG_SZ, sys.argv[0])
                # 清理旧版残留的 Run 键
                try: winreg.DeleteValue(k, 'CalendarApp')
                except: pass
            else:
                try: winreg.DeleteValue(k, '日历')
                except FileNotFoundError: pass
            winreg.CloseKey(k)
        except Exception: pass

    def _sync_autostart(self):
        """启动时同步：如果自启已开但注册表 Run 键缺失或路径不对，补写"""
        if not self.auto_start or sys.platform != 'win32': return
        try:
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r'Software\Microsoft\Windows\CurrentVersion\Run',
                               0, winreg.KEY_READ)
            try:
                v, _ = winreg.QueryValueEx(k, '日历')
                if os.path.normcase(v) != os.path.normcase(sys.argv[0]):
                    winreg.CloseKey(k)
                    self._write_run_key(True)
                else:
                    winreg.CloseKey(k)
            except FileNotFoundError:
                winreg.CloseKey(k)
                self._write_run_key(True)
        except Exception: pass

    def open_settings(self):
        SettingsDialog(self, self).exec_()

    def _load_tasks(self):
        try:
            d = os.path.join(os.environ.get('APPDATA',''),'CalendarApp')
            os.makedirs(d,exist_ok=True)
            f = os.path.join(d,'tasks.json')
            if os.path.exists(f):
                with open(f,'r',encoding='utf-8') as f2: return json.load(f2)
        except: pass
        return {}

    def save_tasks(self):
        try:
            d = os.path.join(os.environ.get('APPDATA',''),'CalendarApp')
            os.makedirs(d,exist_ok=True)
            with open(os.path.join(d,'tasks.json'),'w',encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except: pass

    def _load_settings(self):
        self.bg_color = QColor(int(self.settings.value("bg_red",80)),
                               int(self.settings.value("bg_green",130)),
                               int(self.settings.value("bg_blue",180)))
        self.bg_transparency = int(self.settings.value("bg_transparency",60))
        self.auto_start = bool(self.settings.value("auto_start", False, type=bool))
        self._update_bg()
        g = self.settings.value("geometry")
        if g: self.restoreGeometry(g)

    def _save_settings(self):
        self.settings.setValue("bg_red", self.bg_color.red())
        self.settings.setValue("bg_green", self.bg_color.green())
        self.settings.setValue("bg_blue", self.bg_color.blue())
        self.settings.setValue("bg_transparency", self.bg_transparency)
        self.settings.setValue("geometry", self.saveGeometry())
        self.save_tasks()

    def closeEvent(self, event):
        self._save_settings()
        event.accept()

    def paintEvent(self, event):
        p = QPainter(self); r = self.rect()
        p.setPen(QPen(QColor(255,255,255,80),1))
        s = 15; x,y = r.width()-s, r.height()-s
        p.drawLine(x,y+s,x+s,y+s); p.drawLine(x+s,y,x+s,y+s)
        p.drawLine(x+4,y+s-4,x+s-4,y+s-4); p.drawLine(x+s-4,y+4,x+s-4,y+s-4)


if __name__=='__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    def log_exc(et, ev, tb):
        p = os.path.join(os.environ.get('TEMP','.'),'CalendarApp_crash.log')
        with open(p,'w') as f:
            traceback.print_exception(et, ev, tb, file=f)
        sys.__excepthook__(et, ev, tb)
    sys.excepthook = log_exc
    w = CalendarApp()
    w.show()
    sys.exit(app.exec_())