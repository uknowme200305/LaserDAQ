from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

from datetime import datetime
import os


# =====================================================
# Header / Footer
# =====================================================

def add_page_number(canvas, doc):

    page = canvas.getPageNumber()

    canvas.saveState()

    canvas.setFont("Helvetica", 9)

    canvas.drawRightString(
        7.7 * inch,
        0.4 * inch,
        f"Page {page}"
    )

    canvas.restoreState()


# =====================================================
# Main PDF Function
# =====================================================

def generate_pdf(

    filename,

    laser_results,

    current_data,

    power_data,

    voltage_data,

    temperature_data,

    li_image="li_curve.png",

    vi_image="vi_curve.png",

    simulation_mode=True,

    connected_devices=None

):

    if connected_devices is None:

        connected_devices = {

            "SF6100": True,
            "Maestro": True,
            "TEC3700": True,
            "Avantes": False,
            "Beamage": False

        }

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    doc = SimpleDocTemplate(

        filename,

        rightMargin=30,

        leftMargin=30,

        topMargin=30,

        bottomMargin=30

    )

    elements = []

    # =====================================================
    # UNIVERSITY HEADER
    # =====================================================

    elements.append(

        Paragraph(

            "<b>DELHI TECHNOLOGICAL UNIVERSITY</b>",

            title_style

        )

    )

    elements.append(

        Paragraph(

            "<b>Laser Characterization Software</b>",

            title_style

        )

    )

    elements.append(

        Paragraph(

            "<font size=11>Version 1.0</font>",

            title_style

        )

    )

    elements.append(

        Spacer(1,0.25*inch)

    )

    # =====================================================
    # DATE / TIME
    # =====================================================

    now = datetime.now()

    info_table = [

        ["Date",

         now.strftime("%d-%m-%Y")],

        ["Time",

         now.strftime("%H:%M:%S")],

        ["Mode",

         "Simulation"

         if simulation_mode

         else "Hardware"]

    ]

    info = Table(

        info_table,

        colWidths=[2*inch,3*inch]

    )

    info.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ])

    )

    elements.append(info)

    elements.append(

        Spacer(1,0.3*inch)

    )

    # =====================================================
    # CONNECTED DEVICES
    # =====================================================

    elements.append(

        Paragraph(

            "<b>Connected Instruments</b>",

            heading

        )

    )

    device_table = [

        ["Instrument","Status"]

    ]

    for device,status in connected_devices.items():

        device_table.append([

            device,

            "Connected"

            if status

            else

            "Not Connected"

        ])

    devices = Table(

        device_table,

        colWidths=[3*inch,2.5*inch]

    )

    devices.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("BOTTOMPADDING",(0,0),(-1,0),8),

            ("ALIGN",(0,0),(-1,-1),"CENTER")

        ])

    )

    elements.append(devices)

    elements.append(

        Spacer(1,0.3*inch)

    )

    # =====================================================
    # LASER PARAMETERS
    # =====================================================

    elements.append(

        Paragraph(

            "<b>Laser Parameters</b>",

            heading

        )

    )

    parameter_table = [

        ["Parameter","Value"],

        [

            "Threshold Current (mA)",

            f"{laser_results['threshold_current']:.3f}"

        ],

        [

            "Slope Efficiency (mW/mA)",

            f"{laser_results['slope_efficiency']:.3f}"

        ],

        [

            "Forward Voltage (V)",

            f"{laser_results['forward_voltage']:.3f}"

        ],

        [

            "Differential Resistance (Ω)",

            f"{laser_results['differential_resistance']:.3f}"

        ],

        [

            "Maximum Optical Power (mW)",

            f"{laser_results['maximum_power']:.3f}"

        ],

        [

            "Operating Current (mA)",

            f"{laser_results['operating_current']:.3f}"

        ]

    ]

    parameters = Table(

        parameter_table,

        colWidths=[3.5*inch,2*inch]

    )

    parameters.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

            ("BOTTOMPADDING",(0,0),(-1,0),8),

            ("ALIGN",(0,0),(-1,-1),"CENTER")

        ])

    )

    elements.append(parameters)

    elements.append(

        Spacer(1,0.35*inch)

    )

    # =====================================================
    # L-I CURVE
    # =====================================================

    elements.append(
        Paragraph(
            "<b>L-I Curve</b>",
            heading
        )
    )

    if os.path.exists(li_image):

        elements.append(

            Image(

                li_image,

                width=6.3 * inch,

                height=4.0 * inch

            )

        )

    else:

        elements.append(

            Paragraph(

                "L-I graph not available.",

                normal

            )

        )

    elements.append(
        Spacer(1, 0.25 * inch)
    )

    # =====================================================
    # V-I CURVE
    # =====================================================

    elements.append(

        Paragraph(

            "<b>V-I Curve</b>",

            heading

        )

    )

    if os.path.exists(vi_image):

        elements.append(

            Image(

                vi_image,

                width=6.3 * inch,

                height=4.0 * inch

            )

        )

    else:

        elements.append(

            Paragraph(

                "V-I graph not available.",

                normal

            )

        )

    elements.append(
        Spacer(1, 0.35 * inch)
    )

    # =====================================================
    # RAW MEASUREMENT DATA
    # =====================================================

    elements.append(

        Paragraph(

            "<b>Raw Measurement Data</b>",

            heading

        )

    )

    raw_data = [

        [

            "Current (mA)",

            "Power (mW)",

            "Voltage (V)",

            "Temperature (°C)"

        ]

    ]

    for current, power, voltage, temperature in zip(

        current_data,

        power_data,

        voltage_data,

        temperature_data

    ):

        raw_data.append([

            f"{current:.3f}",

            f"{power:.3f}",

            f"{voltage:.3f}",

            f"{temperature:.3f}"

        ])

    raw_table = Table(

        raw_data,

        colWidths=[1.5 * inch] * 4

    )

    raw_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8)

        ])

    )

    elements.append(raw_table)

    elements.append(
        Spacer(1, 0.25 * inch)
    )

    # =====================================================
    # FOOTER
    # =====================================================

    elements.append(

        Spacer(1, 0.4 * inch)

    )

    elements.append(

        Paragraph(

            "<font size=9>"
            "Generated using Laser Characterization Software v1.0"
            "</font>",

            styles["Normal"]

        )

    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(

        elements,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number

    )