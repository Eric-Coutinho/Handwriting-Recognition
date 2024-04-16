using System;
using System.Drawing;
using System.Diagnostics;
using System.Windows.Forms;
using Timer = System.Windows.Forms.Timer;

namespace Winforms;

public partial class Form1 : Form
{
    PictureBox pb = new PictureBox();
    Bitmap bmp;
    Graphics g;
    Timer tm;
    string uploadedImagePath = "";
    private bool isDrawing = false;
    private bool isErasing = false;
    private Point previousPoint;
    private int thickness = 5;
    private bool isPrinting = false;

    public Button createButton(string text, Point point, Size size)
    {
        Button button = new Button();
        button.Text = text;
        button.Location = point;
        button.Size = size;
        return button;
    }

    public Form1()
    {
        InitializeComponent();

        this.tm = new Timer();
        this.tm.Interval = 20;

        Button uploadButton = createButton("Fazer upload", new Point(10, 75), new Size(100, 30));
        uploadButton.Click += selectImage;
        this.Controls.Add(uploadButton);

        Button printButton = createButton("Tirar print", new Point(10, 110), new Size(100, 30));
        printButton.Click += printScreen;
        this.Controls.Add(printButton);

        this.KeyPreview = true;

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

            if (e.KeyCode == Keys.Oemplus)
                if (this.thickness <= 400)
                    this.thickness += 5;

            if (e.KeyCode == Keys.OemMinus)
                if (this.thickness >= 15)
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
        Font font = new Font("Arial", 12);
        Brush brush = Brushes.Black;

        if (this.isPrinting == false)
        {
            string thicknessText = $"thickness: {thickness}";
            PointF point = new PointF(10, 10);
            g.FillRectangle(Brushes.GhostWhite, point.X, point.Y, 265, 20);
            g.DrawString(thicknessText, font, brush, point);

            string commandsText = "E = Erase\nBackSpace = Clear";
            PointF commandsPoint = new PointF(10, 30);
            g.FillRectangle(Brushes.GhostWhite, commandsPoint.X, commandsPoint.Y, 200, 40);
            g.DrawString(commandsText, font, brush, commandsPoint);

            string arrowsText = "Key + = +5 thickness\nKey- = -10 thickness";
            PointF arrowsPoint = new PointF(160, 30);
            g.FillRectangle(Brushes.GhostWhite, arrowsPoint.X, arrowsPoint.Y, 155, 40);
            g.DrawString(arrowsText, font, brush, arrowsPoint);

            var mode = isErasing ? "Erasing" : "Drawing";
            string modeText = $"mode: {mode}";
            PointF modePoint = new PointF(160, 10);
            g.FillRectangle(Brushes.GhostWhite, modePoint.X, modePoint.Y, 100, 10);
            g.DrawString(modeText, font, brush, modePoint);
        }
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
        if (isDrawing)
        {
            using (Graphics g = Graphics.FromImage(bmp))
            {
                Brush brush = isErasing ? Brushes.White : Brushes.Black;
                var deltaX = e.X - previousPoint.X;
                var deltaY = e.Y - previousPoint.Y;
                var dist = MathF.Sqrt(deltaX * deltaX + deltaY * deltaY);

                for (float d = 0; d < 1; d += 1f / dist)
                {
                    var x = (1 - d) * previousPoint.X + d * e.X;
                    var y = (1 - d) * previousPoint.Y + d * e.Y;
                    g.FillEllipse(brush,
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

    private void printScreen(object sender, EventArgs e)
    {
        isPrinting = true;

        Bitmap screenshotBitmap = new Bitmap(pb.Width, pb.Height);

        using (Graphics g = Graphics.FromImage(screenshotBitmap))
        {
            g.DrawImage(pb.Image, 0, 0, pb.Width, pb.Height);
        }

        using (Graphics g = Graphics.FromImage(screenshotBitmap))
        {
            g.FillRectangle(Brushes.White, 0, 0, 320, 70);
        }

        string filePath = "screenshot.png";
        screenshotBitmap.Save(filePath, System.Drawing.Imaging.ImageFormat.Png);

        MessageBox.Show("Captura de tela salva com sucesso em: " + filePath);

        isPrinting = false;
    }

    private void selectImage(object sender, EventArgs e)
    {
        OpenFileDialog openFileDialog = new OpenFileDialog
        {
            Filter = "Arquivos de imagem|*.jpg;*.jpeg;*.png;*.gif;*.bmp|Todos os arquivos|*.*"
        };

        DialogResult result = openFileDialog.ShowDialog();

        if (result == DialogResult.OK)
        {
            try
            {
                uploadedImagePath = openFileDialog.FileName;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ocorreu um erro ao carregar a imagem: " + ex.Message, "Erro", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }

}