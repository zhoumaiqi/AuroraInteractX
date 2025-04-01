import cv2
import numpy as np
import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
from ultralytics.solutions.solutions import SolutionAnnotator
from ultralytics.utils.downloads import safe_download
from ultralytics.utils.plotting import Annotator, colors

#Download florence model
model_id = "microsoft/Florence-2-large"

# Ensure the runtime is set to GPU in Colab.
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype="auto").eval().cuda()
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

#inference function
def inference(image, task_prompt, text_input=None):
    """
    Performs inference using the given image and task prompt.

    Args:
        image (PIL.Image or tensor): The input image for processing.
        task_prompt (str): The prompt specifying the task for the model.
        text_input (str, optional): Additional text input to refine the task prompt.

    Returns:
        dict: The model's processed response after inference.
    """
    # Combine task prompt with additional text input if provided
    prompt = task_prompt if text_input is None else task_prompt + text_input

    # Generate the input data for model processing from the given prompt and image
    inputs = processor(
        text=prompt,  # Text input for the model
        images=image,  # Image input for the model
        return_tensors="pt",  # Return PyTorch tensors
    ).to("cuda", torch.float16)  # Move inputs to GPU with float16 precision

    # Generate model predictions (token IDs)
    generated_ids = model.generate(
        input_ids=inputs["input_ids"].cuda(),  # Convert text input IDs to CUDA
        pixel_values=inputs["pixel_values"].cuda(),  # Convert image pixel values to CUDA
        max_new_tokens=1024,  # Set maximum number of tokens to generate
        early_stopping=False,  # Disable early stopping
        do_sample=False,  # Use deterministic inference
        num_beams=3,  # Set beam search width for better predictions
    )

    # Decode generated token IDs into text
    generated_text = processor.batch_decode(
        generated_ids,  # Generated token IDs
        skip_special_tokens=False,  # Retain special tokens in output
    )[0]  # Extract first result from batch

    # Post-process the generated text into a structured response
    parsed_answer = processor.post_process_generation(
        generated_text,  # Raw generated text
        task=task_prompt,  # Task type for post-processing
        image_size=(image.width, image.height),  # Original image dimensions for scaling output
    )

    return parsed_answer  # Return the final processed output


#从google云端硬盘读取图片
from google.colab import drive

def read_image(filename=None):
    """
    读取图片，如果 filename 为 None，则读取云端硬盘中的 zoo.jpg；
    否则读取 filename 指定的图片。

    Args:
        filename (str, optional): 图片文件的路径. Defaults to None.

    Returns:
        PIL.Image: 读取到的图片对象。
    """
    if filename is None:
        # 读取云端硬盘中的 zoo.jpg
        drive.mount('/content/drive')  # 挂载云端硬盘
        image_path = "/content/drive/MyDrive/Colab Notebooks/imag/stairs.jpg"  # 云端硬盘中 zoo.jpg 的路径
    else:
        # 读取 filename 指定的图片
        image_path = filename 

    # 读取图片并转换为 PIL 格式
    return Image.fromarray(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))


## Read the image
"""
# Result format 😀
{
    "<OD>": {
        "bboxes": [[x1, y1, x2, y2], ...],
        "labels": ["label1", "label2", ...]
    }
}
"""

task_prompt = "<OD>"
image = read_image()

results = inference(image, task_prompt)["<OD>"]

# Plot the results on an image
annotator = Annotator(image)  # initialize Ultralytics annotator

for idx, (box, label) in enumerate(zip(results["bboxes"], results["labels"])):
    annotator.box_label(box, label=label, color=colors(idx, True))

Image.fromarray(annotator.result())  # display the output