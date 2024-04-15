# Sundara - Collaborative Mining Network


## Introduction

**Background**

Many subnets in Bittensor now require GPUs to perform inference tasks and receive rewards based on performance. However, many excellent model developers do not have enough GPUs to join the subnet as miners. The high cost of computing power equipment has become a barrier for more excellent developers to enter the AI ecosystem.

**What is Sundara**

Sundara is building a decentralized collaborative mining network that aggregates and optimizes GPU resources to provide efficient and reliable computing power for AI tasks, initially focusing on model inference and eventually expanding to support more complex tasks like model training.

With Sundara, users can join Bittensor subnets as a light node and cooperate with Sundara subnet for mining. This allows top models to be rapidly integrated into the Bittensor network without concern for GPU limitations. Models that yield better results receive more rewards, incentivizing AI developers to continually enhance their models.

Sundara will keep updating the scheduling algorithm on the Bittensor subnet to make sure the whole network of computing power scheduling is stable and available.

## System Design

Sundara provides a computing power liquidity pool to collaboratively complete AI inference tasks. Other Bittensor subnets and projects only need to maintain their own lightweight nodes, and distribute heavy computing tasks to the Sundara subnet for collaboration.

![Sundara System Design](https://github.com/sundara-io/subnet-sundara/assets/6276527/0a904bc2-0762-4005-ad1f-07715001dee5)

The workflow of Sundara is roughly divided into these steps.:

1. **Preparation in Advance**: AI models will be registered in advance in the Sundara Model Registry. Physical devices in Sundara won't directly run the models, but will operate in the form of containers when needed. Containers provide a uniform operating environment for AI models, thus facilitating convenient scheduling and scale out.
2. **Proxy Computing Request**: When the light node undertakes a computing task related to the AI model, it forwards this task to the Sundara validator. The validator is responsible for accepting external task requests. It parses the model name from parameters and selects several qualified miners for task execution. 
3. **Perform computing tasks**: The miners receive the computing task, will run the model in container locally, and return the results to the validator. The miners are not limited to the model and can pull the image from the model registry at any time to undertake AI inference tasks. 
4. **Verify the results**: After receiving the results from the miners, the validator will verify whether their results are correct. Under the condition of consistent input parameters and a fixed random seed, the AI model will definitely return consistent results.
5. **Reward Model**: Rewards will be issued based on the consistency of the results and the time consumed. If the validator verifies that the results are inconsistent, there will be no rewards. If the results are consistent, ranking will be performed based on the time consumed.
6. **Metrics and Orchestration:** Sundara will keep collecting metrics and automatically adjust the model tasks according to the load situation. If there are unavailable or dishonest nodes in the network, Orchestrator will immediately replace the nodes to ensure the stability and availability of the entire network.

## Technical features

- **Scheduling to improve utilization rate**: In Sundara, the device will not be bound with a certain model. We use the lightweight operation method of containers, allowing each machine to run multiple models, thus intelligently scheduling according to the needs of the scenario, reducing the idle time of the device, and improving the utilization rate of computing power.
- **Orchestration to ensure availability**: Sundara will keep collecting metrics from AI model containers and replace unavailable nodes with new ones. All users need to do is provide a AI model. Sundara will ensure the availability of these instances through real-time metrics monitoring and automatic orchestration.
- **GPU Virtualization to run in parallel**: Sundara will also further optimize on the GPU level. Through vGPU and virtualization technology, large-scale GPU devices are broken down into vGPUs more suitable for small model inference scenarios, in order to further improve the usage rate of computing power and increase the computing power task carrying capacity of the platform.

## Guide

**Validator Installation**

Please see [Validator Setup](./docs/quickstart.md#validator-setup).

**Miner Installation**

Please see [Miner Setup](./docs/quickstart.md#miner-setup).