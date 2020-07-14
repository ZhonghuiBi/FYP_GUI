import sys,math
import res
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtWidgets import QApplication,QLabel,QPushButton,QWidget,QVBoxLayout,QHBoxLayout,QLineEdit,QGridLayout,QComboBox,QFrame,QGroupBox,QRadioButton,QFileDialog
from PyQt5.QtChart import QChartView,QChart,QLineSeries,QValueAxis

class Demo(QWidget,QFont):
    def __init__(self):
        super(Demo,self).__init__()     #子类调用父类的方法
        self.BuildUI()                  #构造界面
        self.CreatChart()               #创建曲线
        self.connection()

##==============自定义功能函数============
    def BuildUI(self):   ##构造界面
        self.resize(800, 600)
        self.setFont(QFont("黑体", 10.5))  ##设置字体
        self.setWindowTitle("水工标准设计反应谱v1.1(Hs小毕)")  ##s设置窗口标题
        self.setWindowIcon(QIcon(':/fyp.ico'))

        # 定义控件
        #定义“输入”控件===========================
        self.label1 = QLabel("水工建筑物类型", self)
        # 标准设计反应谱最大值的代表值
        BEITA = ["土石坝", "重力坝", "拱坝", "水闸|进水塔|边坡|其他"]
        self.comboBox1 = QComboBox()
        self.comboBox1.addItems(BEITA)
        self.comboBox1.setCurrentIndex(1)  # 设置默认值
        self.label2 = QLabel("特征周期Tg(s)", self)
        self.line2 = QLineEdit()
        self.line2.setPlaceholderText("单位(s)")
        self.label3 = QLabel("加速度幅值A(g)", self)
        self.line3 = QLineEdit()
        self.line3.setPlaceholderText("单位(g)")
        self.groupbox_1 = QGroupBox('输入数据', self)
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label1)
        self.v_layout.addWidget(self.comboBox1)
        self.v_layout.addWidget(self.label2)
        self.v_layout.addWidget(self.line2)
        self.v_layout.addWidget(self.label3)
        self.v_layout.addWidget(self.line3)
        self.groupbox_1.setLayout(self.v_layout)

        #定义“生成”控件===========================
        self.v1_layout = QVBoxLayout()
        self.groupbox_2 = QGroupBox('生成曲线', self)
        self.button1 = QPushButton("生成曲线",self)
        self.v1_layout.addWidget(self.button1)
        self.groupbox_2.setLayout(self.v1_layout)

        #定义“输出单位”控件
        self.groupbox_3 = QGroupBox('输出单位', self)
        self.h_layout = QHBoxLayout()
        self.unit_g = QRadioButton('g', self)
        self.unit_g.setChecked(True)                #设置单位“g”为默认
        self.unit_m = QRadioButton('m/sec2', self)
        self.unit_mm = QRadioButton('mm/sec2', self)
        self.h_layout.addWidget(self.unit_g)
        self.h_layout.addWidget(self.unit_m)
        self.h_layout.addWidget(self.unit_mm)
        self.groupbox_3.setLayout(self.h_layout)
        #定义输出的列数
        self.groupbox_4 = QGroupBox('输出列数', self)
        self.h1_layout = QHBoxLayout()
        self.list2 = QRadioButton('时间|谱值')
        self.list2.setChecked(True)  # 设置时间|谱值为默认
        self.list1 = QRadioButton('谱值')
        self.h1_layout.addWidget(self.list2)
        self.h1_layout.addWidget(self.list1)
        self.groupbox_4.setLayout(self.h1_layout)
        #输出时间间隔
        self.groupbox_5 = QGroupBox('输出时间间隔(s)', self)
        self.v2_layout = QHBoxLayout()
        self.Dtime = QRadioButton('0.01')
        self.Dtime.setChecked(True)  # 设置0.01s为默认
        self.Dtime_Edit = QLineEdit()
        self.Dtime1 = QRadioButton(self.Dtime_Edit)
        self.v2_layout.addWidget(self.Dtime)
        self.v2_layout.addWidget(self.Dtime1)
        self.v2_layout.addWidget(self.Dtime_Edit)
        self.groupbox_5.setLayout(self.v2_layout)
        #定义输出的文件选择
        self.groupbox_6 = QGroupBox('输出文件', self)
        self.v3_layout = QVBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.Enter = QPushButton('点击输出',self)
        self.out_line=QLineEdit()
        self.out_select=QPushButton('浏览',self)
        self.h3_layout.addWidget(self.out_line)
        self.h3_layout.addWidget(self.out_select)
        self.v3_layout.addLayout(self.h3_layout)
        self.v3_layout.addWidget(self.Enter)
        self.groupbox_6.setLayout(self.v3_layout)

        # 定义绘图控件===========================
        self.chartView = QChartView()  # 创建 ChartView
        self.v6_layout = QVBoxLayout()
        self.v6_layout.addWidget(self.groupbox_1)
        self.v6_layout.addWidget(self.groupbox_2)
        self.v6_layout.addWidget(self.groupbox_3)
        self.v6_layout.addWidget(self.groupbox_4)
        self.v6_layout.addWidget(self.groupbox_5)
        self.v6_layout.addWidget(self.groupbox_6)

        self.h4_layout = QHBoxLayout()
        self.h4_layout.addLayout(self.v6_layout)
        self.h4_layout.addWidget(self.chartView)
        self.setLayout(self.h4_layout)

    def CreatChart(self):
        self.chart = QChart()  # 创建 Chart
        self.chart.setTitle("反应谱曲线")
        self.chartView.setChart(self.chart)  # Chart添加到ChartView
        # 创建曲线序列
        self.series0 = QLineSeries()
        self.chart.addSeries(self.series0)  # 序列添加到图表
        self.chart.createDefaultAxes()
        ##创建坐标轴
        self.axisX = QValueAxis()  # X 轴
        self.axisX.setTitleText("T(s)")  # 标题
        self.axisX.setLabelFormat("%.1f")     #标签格式
        self.axisX.setTickCount(5)           #主分隔个数
        self.axisX.setMinorTickCount(4)
        self.axisY=QValueAxis()  # Y 轴
        self.axisY.setTitleText("Se/g")
        self.axisY.setTickCount(5)
        self.axisY.setMinorTickCount(4)
        self.axisY.setLabelFormat("%.2f")     #标签格式
        # 为序列设置坐标轴
        self.chart.setAxisX(self.axisX, self.series0)  # 为序列设置坐标轴
        self.chart.setAxisY(self.axisY, self.series0)

    def PrepareData(self):
        """
        定义绘图中的数据
        """
        # 序列添加数值
        Str_dict={"土石坝":1.6, "重力坝":2, "拱坝":2.5, "水闸|进水塔|边坡|其他":2.25}
        Str_list =self.comboBox1.currentText()
        BETA_Data = Str_dict[Str_list]
        # 特征周期
        TG = float(self.line2.text())
        # 加速度幅值
        PGA = float(self.line3.text())
        t = 0
        intv = 0.01
        pointCount = 301
        self.series0.clear()   #清楚数据========
        for T in range(pointCount):
            T= round(T * intv,2)
            if T <= 0.1:
                y1 = (BETA_Data-1)/(0.1-0)*T+1
            elif 0.1<T and T <= TG:
                y1= BETA_Data
            else:
                y1 = BETA_Data*(TG/T)**0.6
            y1 = y1 * PGA
            self.series0.append(T, y1)
        #设置坐标轴范围=========================
        self.axisX.setRange(0,3)
        self.axisY.setRange(0,BETA_Data*PGA+1)

    def outputfilename(self):
        """
        定义输出路径
        """
        dlg = QFileDialog()
        filt = "Srf Files(*.Srf);;Text Files (*.txt);;All Files (*)"
        fileName, _ =dlg.getSaveFileName(self, "另存为文件", ".",filt)
        self.out_line.setText(fileName)

    def Output_Data(self):
        """
        定义输出的数据
        """
        # 序列添加数值
        Str_dict={"土石坝":1.6, "重力坝":2, "拱坝":2.5, "水闸|进水塔|边坡|其他":2.25}
        Str_list =self.comboBox1.currentText()
        BETA_Data = Str_dict[Str_list]
        # 特征周期
        TG = float(self.line2.text())
        # 加速度幅值
        PGA = float(self.line3.text())
        # 输出单位
        if self.unit_g.isChecked()==True:
            UNIT = 1
        elif self.unit_g.isChecked()==True:
            UNIT = 9.81
        else:
            UNIT = 9810
        # 输出间隔
        if self.Dtime.isChecked()==True:
            intv = 0.01
        else:
            intv = float(self.Dtime_Edit.text())
        pointCount = 301
        fileNameout = QLineEdit.text(self.out_line)
        with open(fileNameout, 'w', encoding='gbk') as f_out:
            for T in range(pointCount):
                T = round(T * intv, 2)
                if T <= 0.1:
                    y1 = (BETA_Data - 1) / (0.1 - 0) * T + 1
                elif 0.1 < T and T <= TG:
                    y1 = BETA_Data
                else:
                    y1 = BETA_Data * (TG / T) ** 0.6
                y1 = y1 * PGA * UNIT
                if self.list2.isChecked()==True:
                    f_out.write(f"{T}\t\t{y1}\n")
                else:
                    f_out.write(f"{y1}\n")
    def connection(self):
        """
        槽函数
        """
        self.button1.clicked.connect(lambda: self.PrepareData())
        self.out_select.clicked.connect(lambda: self.outputfilename())
        self.Enter.clicked.connect(lambda: self.Output_Data())

if __name__=='__main__':
    app = QApplication(sys.argv)
    lable = Demo()
    lable.show()
    sys.exit(app.exec())




