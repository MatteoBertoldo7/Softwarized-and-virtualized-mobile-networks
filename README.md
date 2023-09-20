# Softwarized-and-virtualized-mobile-networks

Project Description:
This project aims to develop a dynamic network slicing solution within a Software-Defined Networking (SDN) environment. Network slicing is a key concept in modern networking, allowing the creation of isolated virtual networks with specific characteristics and Quality of Service (QoS) requirements. The primary goals of this project are as follows:

1. Network Slicing Setup:

Implement a network slicing approach that enables the dynamic creation, activation, and deactivation of network slices.
Use a single SDN controller, such as RYU, to manage the network.
Define and describe network slice templates that allow the identification of flows, network topology, and percentage of link capacity for each slice.
2. QoS Management:

Define and configure specific QoS policies for each network slice. For example, "Smart Traffic" may require low latency, "Public Safety" may require high reliability, and "IoT Monitoring" may require high bandwidth.
Implement policies that dynamically allocate network resources to maintain the desired QoS for each slice.
3. Slice-Optimization Scenarios:

Develop scenarios where network resources can be dynamically reallocated to optimize network performance. For instance, migrating a server to maximize throughput or minimize delay via northbound scripts.
Consider environmental changes, such as link failures or the introduction of new traffic, and adapt the network accordingly.
4. Tools and Technologies:

Utilize ComNetsEmu, an SDN/NFV network emulator that extends Mininet's capabilities, for network emulation.
Key tools and technologies include Mininet for creating virtual network entities, RYU as the SDN controller, and Wireshark for packet analysis during emulation.
5. Infrastructure Design:

Design a reference network infrastructure that includes switches, base stations, and data centers.
Configure the network infrastructure parameters, such as the number of slices, datacenter locations, and user-to-base station mappings, via a configuration file.
6. Project Workflow:

Deploy the network using RYU controller with specified configurations.
Interact with the deployed network through a Mininet client to monitor and control network slices.
Implement custom flow rules or limitations using Ryu's SDN controller capabilities.
7. Slicing Scenarios:

Develop and demonstrate different network slicing scenarios, each with unique QoS requirements and optimization goals.
Evaluate the performance and effectiveness of the dynamic network slicing and QoS management.
8. Documentation and Reporting:

Document the project thoroughly, including network configurations, slice templates, and QoS policies.
Prepare reports and findings based on the project's evaluation and testing results.
By implementing dynamic network slicing and efficient QoS management, this project aims to showcase the advantages of SDN in optimizing network resources and providing tailored services for various applications and traffic types.
