using Python.Runtime;

Runtime.PythonDLL = "python311.dll";
PythonEngine.Initialize();

dynamic tf = Py.Import("tensorflow");
dynamic np = Py.Import("numpy");

dynamic model = tf.keras.models.load_model("98-99.keras");

dynamic list = new PyList();
list.append(tf.keras.utils.load_img("001.png"));

dynamic data = np.array(list);
dynamic result = model.predict(data);
dynamic maxIndex = np.argmax(result);
Console.WriteLine(result);
Console.WriteLine("Maior Index: " + maxIndex.ToString());

PythonEngine.Shutdown();