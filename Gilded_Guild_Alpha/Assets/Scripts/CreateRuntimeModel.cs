using UnityEngine;
using Unity.InferenceEngine;

public class CreateRuntimeModel : MonoBehaviour
{
    public ModelAsset modelAsset;
    public float[] UserInput = new float[463];
    Model runtimeModel;
    Worker worker;
    public float[] results;


    public void AcceptUserInput(float[] inp) { 
        UserInput = inp;
    }
    public float[] GetResults() { 
        return results;
    }
    void Start()
    {
        runtimeModel = ModelLoader.Load(modelAsset);
        GetBotAction();
    }
    public void GetBotAction() {
        // modified from https://docs.unity3d.com/Packages/com.unity.ai.inference@2.2/manual/workflow-example.html

        FunctionalGraph graph = new FunctionalGraph();
        FunctionalTensor[] input = graph.AddInputs(runtimeModel);
        FunctionalTensor[] outputs = Functional.Forward(runtimeModel, input);
        FunctionalTensor softmax = Functional.Softmax(outputs[0]);

        // Create a model with softmax by compiling the functional graph.
        graph.AddOutput(softmax);
        runtimeModel = graph.Compile();

        // Create input data as a tensor
        Tensor<float> inputTensor = new Tensor<float>(new TensorShape(1, 463), UserInput);

        // Create an engine
        worker = new Worker(runtimeModel, BackendType.GPUCompute);

        // Run the model with the input data
        worker.Schedule(inputTensor);

        // Get the result
        Tensor<float> outputTensor = worker.PeekOutput() as Tensor<float>;

        // outputTensor is still pending
        // Either read back the results asynchronously or do a blocking download call
        results = outputTensor.DownloadToArray();
        worker.Dispose();
        inputTensor.Dispose();
        outputTensor.Dispose();
    }
    void OnDisable()
    {
        // Tell the GPU we're finished with the memory the engine used
        worker.Dispose();
    }
}
