using System.Drawing;
using System.Windows.Forms;
using System;
using Timer = System.Windows.Forms.Timer;

namespace Winforms;

public partial class Form1 : Form
{
    PictureBox pb = new PictureBox();
    Bitmap bmp;
    Graphics g;
    Timer tm;
    private bool isDrawing = false;
    private bool isErasing = false;
    private Point previousPoint;
    private int thickness = 5;

    public Form1()
    {
        InitializeComponent();

        this.tm = new Timer();
        this.tm.Interval = 20;

        this.BackColor = Color.White;

        this.WindowState = FormWindowState.Maximized;
        this.FormBorderStyle = FormBorderStyle.None;

        this.Controls.Add(pb);
        pb.Dock = DockStyle.Fill;

        pb.MouseDown += pb_MouseDown;
        pb.MouseMove += pb_MouseMove;
        pb.MouseUp += pb_MouseUp;

        this.KeyDown += (o, e) =>
        {
            if (e.KeyCode == Keys.Escape)
                Application.Exit();

            if (e.KeyCode == Keys.Back)
                clearPanel();

            if (e.KeyCode == Keys.Up)
                this.thickness += 5;

            if (e.KeyCode == Keys.Down)
                this.thickness -= 10;

            if (e.KeyCode == Keys.E)
            {
                if (isErasing == false)
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
        };

        tm.Tick += (o, e) =>
        {
            Frame();
            pb.Refresh();
        };

        tm.Start();
    }

    void Frame()
    {
        string thicknessText = $"thickness: {thickness}";
        Font font = new Font("Arial", 12);
        Brush brush = Brushes.Black;
        PointF point = new PointF(10, 10);
        g.FillRectangle(Brushes.GhostWhite, point.X, point.Y, 265, 20);
        g.DrawString(thicknessText, font, brush, point);

        string commandsText = "E = Erase\nBackSpace = Clear";
        Font commandsFont = new Font("Arial", 12);
        Brush commandsBrush = Brushes.Black;
        PointF commandsPoint = new PointF(10, 30);
        g.FillRectangle(Brushes.GhostWhite, commandsPoint.X, commandsPoint.Y, 200, 40);
        g.DrawString(commandsText, commandsFont, commandsBrush, commandsPoint);

        string arrowsText = "Arrow Up = +5 thickness\nArrow Down = -10 thickness";
        Font arrowsFont = new Font("Arial", 12);
        Brush arrowsBrush = Brushes.Black;
        PointF arrowsPoint = new PointF(160, 30);
        g.FillRectangle(Brushes.GhostWhite, arrowsPoint.X, arrowsPoint.Y, 210, 40);
        g.DrawString(arrowsText, arrowsFont, arrowsBrush, arrowsPoint);

        var mode = isErasing ? "Erasing" : "Drawing";
        string modeText = $"mode: {mode}";
        Font modeFont = new Font("Arial", 12);
        Brush modeBrush = Brushes.Black;
        PointF modePoint = new PointF(160, 10);
        g.FillRectangle(Brushes.GhostWhite, modePoint.X, modePoint.Y, 100, 10);
        g.DrawString(modeText, modeFont, modeBrush, modePoint);
    }

    private void clearPanel()
    {
        this.thickness = 5;
        g.Clear(Color.White);
        pb.Invalidate();
    }

    private void pb_MouseDown(object sender, MouseEventArgs e)
    {
        isDrawing = true;
        previousPoint = e.Location;
    }

    private void pb_MouseUp(object sender, MouseEventArgs e)
    {
        isDrawing = false;
    }
    private void pb_MouseMove(object sender, MouseEventArgs e)
    {
        if (isDrawing && isErasing == false)
        {
            using (Graphics g = Graphics.FromImage(bmp))
            {
                var deltaX = e.X - previousPoint.X;
                var deltaY = e.Y - previousPoint.Y;
                var dist = MathF.Sqrt(deltaX * deltaX + deltaY * deltaY);

                for (float d = 0; d < 1; d += 1f / dist)
                {
                    var x = (1 - d) * previousPoint.X + d * e.X;
                    var y = (1 - d) * previousPoint.Y + d * e.Y;
                    g.FillEllipse(Brushes.Black,
                        x - thickness / 2,
                        y - thickness / 2,
                        thickness, thickness
                    );
                }

                previousPoint = e.Location;
                pb.Refresh();
            }
        }
        else if (isDrawing && isErasing == true)
        {
            using (Graphics g = Graphics.FromImage(bmp))
            {
                var deltaX = e.X - previousPoint.X;
                var deltaY = e.Y - previousPoint.Y;
                var dist = MathF.Sqrt(deltaX * deltaX + deltaY * deltaY);

                for (float d = 0; d < 1; d += 1f / dist)
                {
                    var x = (1 - d) * previousPoint.X + d * e.X;
                    var y = (1 - d) * previousPoint.Y + d * e.Y;
                    g.FillEllipse(Brushes.White,
                        x - thickness / 2,
                        y - thickness / 2,
                        thickness, thickness
                    );
                }

                previousPoint = e.Location;
                pb.Refresh();
            }
        }
    }

}