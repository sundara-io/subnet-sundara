## **Introduction**

**Background**

For developers, the computing tasks of subnet generally require high-configuration GPU devices, which has a high entry barrier. Even if model developers have developed excellent AI models, they can't join other subnets in bittensor, and can't earn income from their own models.

**What is Sundara**

Sundara is a collaborative mining protocol that provides accessible and adaptable hardware services for the forthcoming open AI network.

We're constructing a distributed computing power scheduling system, designed to substantially reduce the barriers to entry for AI computational resources. This empowers proficient developers within the ML community to contribute to AI development, while also making top-tier AI models accessible to a broader audience. Ultimately, our goal is to make AI widely available to consumers.

We aspire to enable exceptional model developers to concentrate on model optimization and iteration by providing collaborative mining opportunities for computational power.

With the introduction of the Sundara subnet, users can now join the subnet and collaborate with Sundara in mining activities. This facilitates rapid deployment of exceptional models onto the Bittensor network, liberating them from GPU device constraints. Superior models, owing to their closer approximation to accurate results, are poised to receive greater rewards, thereby incentivizing AI model developers to iteratively develop and refine more outstanding models.

Sundara will continuously iterate and evolve the scheduling algorithm through the Bittensor subnet, to ensure the stability and availability of the entire computing power scheduling network.

## Collaborative Mining

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/774f85dd-b10c-4c33-a581-451afbd22b88/3935490a-894c-4603-acf1-315aff9d491d/Untitled.png)

We provide a computing power liquidity pool to collaboratively complete computing tasks. Other Bittensor subnets and projects can focus on the business logic itself, only need to maintain their own lightweight nodes, and allocate heavy computing tasks to the Sundara subnet for collaboration.

We will define a set of communication schemas and interfaces for external parties to publish computing tasks to Sundara, validators to accept tasks, and distribute them to the underlying miner nodes.
We will distribute tasks to the underlying computing power equipment network through scheduling algorithms, improve the utilization rate of individual devices through virtualization technology, smooth out fluctuations in call volume and improve the capacity of the entire network by supporting multi-model inference, and ensure the high availability of the entire network through real-time monitoring and automatic scaling in and out.

- Validator: Accepts external task requests, parses parameters to select a qualified miner to execute the task, and is responsible for verifying the consistency of the model results after receiving them, confirming that the miner has completed the task as required.
- Miner: The miner is not limited to the model, and can pull the image from the model registry at any time to gain the ability to undertake computing tasks. Upon receiving the validator's scheduling, it will match the model and perform the computing task, and return the result.
- Reward Model: Rewards will be issued based on the consistency of the results and the time consumed. If the validator verifies that the results are inconsistent, there will be no rewards. If the results are consistent, ranking will be performed based on the time consumed.

### **Technical Advantages**

- Traditional computing networks aggregate computing power, with a focus on connecting computing power networks and building computing power clusters. However, they cannot improve the utilization rate of computing power equipment. For some scenarios, such as peaks and troughs in call volumes and high computing power devices running low computing power tasks for a long time, there is a huge waste of computing power.
- Sundara will schedule computing power from the task dimension, prioritizing matching with the most suitable computing power resources to avoid waste of computing power. At the same time, it will also try to reuse computing power devices. A single device can run multiple models, meeting the various needs of different users in different scenarios, thereby providing more stable and cheaper computing power resources.
- Sundara will also further optimize on the GPU level. Through vGPU and virtualization technology, large-scale GPU devices are broken down into vGPUs more suitable for small model inference scenarios, in order to further improve the usage rate of computing power and increase the computing power task carrying capacity of the platform.
- For large-scale training tasks, Sundara will provide task slice clusters based on vGPU. Through task decomposition and combination by layer/data, it meets the needs of large-scale model training.

## Guide

**Validator Installation**

Please see [Validator Setup](./docs/quickstart.md#validator-setup) in the [quick start guide](./docs/quickstart.md).

**Miner Installation**

Please see [Miner Setup](./docs/quickstart.md#miner-setup) in the [quick start guide](./docs/quickstart.md)