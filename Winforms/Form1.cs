using System;
using System.Drawing;
using System.Windows.Forms;

namespace Winforms;

public partial class Form1 : Form
{
    PictureBox pb = new PictureBox();
    Bitmap bmp;
    Graphics g;
    private bool isDrawing = false;
    private bool isErasing = false;
    private Point previousPoint;
    private int thickness = 5;

    public Form1()
    {
        InitializeComponent();

        this.BackColor = Color.White;

        this.WindowState = FormWindowState.Maximized;
        this.FormBorderStyle = FormBorderStyle.None;

        this.MouseDown += panel1_MouseDown;
        this.MouseMove += panel1_MouseMove;
        this.MouseUp += panel1_MouseUp;

        this.KeyDown += (o, e) =>
        {
            if (e.KeyCode == Keys.Escape)
                Application.Exit();

            if (e.KeyCode == Keys.Back)
                clearPanel();

            if (e.KeyCode == Keys.Up)
                this.thickness += 5;

            if (e.KeyCode == Keys.Down)
                this.thickness -= 5;

            if (e.KeyCode == Keys.E) {
                if(isErasing == false)
                    this.isErasing = true;
                else
                    this.isErasing = false;
            }

        };

        this.Load += (o, e) =>
        {
            this.bmp = new Bitmap(pb.Width, pb.Height);
            g = Graphics.FromImage(bmp);
            g.Clear(Color.White);
            this.pb.Image = bmp;

            Onstart();
        };
    }

    void Onstart()
    {

    }

    private void clearPanel()
    {
        this.Invalidate();
    }

    private void panel1_MouseDown(object sender, MouseEventArgs e)
    {
        isDrawing = true;
        previousPoint = e.Location;
    }

    private void panel1_MouseUp(object sender, MouseEventArgs e)
    {
        isDrawing = false;
    }
    private void panel1_MouseMove(object sender, MouseEventArgs e)
    {
        if (isDrawing && isErasing == false)
        {
            using (Graphics g = this.CreateGraphics())
            {
                using (Pen pen = new Pen(Color.Black, thickness))
                {
                    g.DrawLine(pen, previousPoint, e.Location);
                }
                previousPoint = e.Location;
            }
        }

        else if (isDrawing && isErasing == true)
        {
            using (Graphics g = this.CreateGraphics())
            {
                using (Pen pen = new Pen(Color.White, thickness + 5))
                {
                    g.DrawLine(pen, previousPoint, e.Location);
                }
                previousPoint = e.Location;
            }
        }
    }

}