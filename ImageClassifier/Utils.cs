using System;
using System.IO;

public static class Utils
{
    public static void MoveFile(string origin_path, string destination_path, string new_name = null)
    {
        string file_name = Path.GetFileName(origin_path);
        string folder = Path.GetDirectoryName(destination_path);
        if (!Directory.Exists(folder))
            Directory.CreateDirectory(folder);

        File.Move(origin_path, folder + "\\" + (new_name ?? file_name));
    }
}