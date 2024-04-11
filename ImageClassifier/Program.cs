using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;

string origin = ".\\ImageClassifier\\";
if (Directory.Exists($"{origin}Img"))
    Directory.Delete($"{origin}Img", true);
if (File.Exists($"{origin}english.csv"))
    File.Delete($"{origin}english.csv");
ZipFile.ExtractToDirectory($"{origin}images.zip", $"{origin}");

try
{
    string[] images = Directory.GetFiles($"{origin}Img");
    Dictionary<string, string> csv = new Dictionary<string, string>();

    using (var reader = new StreamReader($"{origin}english.csv"))
    {
        string[] line;
        while (!reader.EndOfStream)
        {
            line = reader.ReadLine().Split(',');
            if (!line[0].Contains("Img"))
                continue;
            
            if (line.Length != 2)
                throw new Exception("incorrect quantity of items on line [" + String.Join(", ", line) + "]");

            char charac = line[1][0];
            csv[origin + line[0].Replace("/", "\\")] = $".\\Img\\{(int)charac}\\";
        }
    }

    foreach (var image in images)
        Utils.MoveFile(image, csv[image], Path.GetFileName(image).Split('-')[^1]);
}
catch (Exception e)
{
    Console.WriteLine("Error: " + e.Message);
    Console.ReadLine();
}