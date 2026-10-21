# Research page editorial notes

Last curated: 2026-09-14. Direction order updated: 2026-09-20.

The page synthesizes research represented in the repository from 2019 onward. It is an editorial overview, not an exhaustive or mutually exclusive classification. Existing publication filters remain the detailed taxonomy. The overview is native HTML/CSS so its labels remain readable and its directions are clickable.

The reference is https://wan-research-group.github.io/research.html. Its overview → directions → representative publications structure informed the page; the research descriptions and five-direction grouping are original to this site.

## Topic mapping

| Research-page direction | Existing publication topics |
| --- | --- |
| AI Accelerators & Automated Design | AI/ML Accelerators, AI-Assisted Design |
| Distributed AI & Datacenter Co-design | Distributed AI Systems |
| Efficient & Compositional AI Systems | Efficient LLM & Model Inference, Compositional & Cognitive AI, Edge & Embodied Computing |
| Secure & Private Computing | Privacy & Security |
| Interconnects, Memory & Chiplet Systems | Interconnection & On-Chip Networks, Memory & Virtual-Memory Systems, Emerging Tech & Packaging |
| Shared research infrastructure | Simulation & Benchmarking; relevant to every direction |

## Selection and metadata

Representative work is ordered from earlier to later contributions within each theme. Papers were selected for methodological breadth and continuity, not citation rank. Book chapters, duplicate entries, and lab reports were not used as representative papers. A paper may be relevant to more than one direction.

Venue overrides for recent accepted papers follow VERIFIED_META in assets/js/publications.js, consistent with the existing News and Publications pages. MCMComm remains explicitly labeled arXiv 2025. Full titles preserve the source wording, with acronym capitalization normalized; the MAESTRO title uses the full author-posted title. Source records and primary links below support future updates.

## AI Accelerators & Automated Design

- **Understanding Reuse, Performance, and Hardware Cost of DNN Dataflows: A Data-Centric Approach Using MAESTRO** — MICRO 2019
  - Repository record: assets/scripts/pub_list/htmls/synergy_2019/paper_scholar2019_understanding-reuse-performance-and-hardware-cost-of.html
  - Paper: https://arxiv.org/abs/1805.02566
- **SIGMA: A Sparse and Irregular GEMM Accelerator with Flexible Interconnects for DNN Training** — HPCA 2020
  - Repository record: assets/scripts/pub_list/htmls/synergy_2020/paper_scholar2020_sigma-a-sparse-and-irregular-gemm-accelerator-with-f.html
  - Paper: https://doi.org/10.1109/HPCA47549.2020.00015
- **ConfuciuX: Autonomous Hardware Resource Assignment for DNN Accelerators using Reinforcement Learning** — MICRO 2020
  - Repository record: assets/scripts/pub_list/htmls/synergy_2020/paper_scholar2020_confuciux-autonomous-hardware-resource-assignment-fo.html
  - Paper: https://arxiv.org/abs/2009.02010
- **FEATHER: A Reconfigurable Accelerator with Data Reordering Support for Low-Cost On-Chip Dataflow Switching** — ISCA 2024
  - Repository record: assets/scripts/pub_list/htmls/synergy_2024/paper_tong2024feather.html
  - Paper: https://dl.acm.org/doi/10.1109/ISCA59077.2024.00024
- **MicroScopiQ: Accelerating Foundational Models through Outlier-Aware Microscaling Quantization** — ISCA 2025
  - Repository record: assets/scripts/pub_list/htmls/synergy_2025/paper_ramachandran2025microscopiq.html
  - Paper: https://dl.acm.org/doi/pdf/10.1145/3695053.3730989
- **AIRCHITECT v2: Learning the Hardware Accelerator Design Space Through Unified Representations** — DATE 2025
  - Repository record: assets/scripts/pub_list/htmls/synergy_2025/paper_seo2025airchitect.html
  - Paper: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10993035

## Distributed AI & Datacenter Co-design

- **ASTRA-sim: Enabling SW/HW Co-Design Exploration for Distributed DL Training Platforms** — ISPASS 2020
  - Repository record: assets/scripts/pub_list/htmls/synergy_2020/paper_scholar2020_astra-sim-enabling-sw-hw-co-design-exploration-for-d.html
  - Paper: https://doi.org/10.1109/ISPASS48437.2020.00018
- **Themis: A Network Bandwidth-Aware Collective Scheduling Policy for Distributed Training of DL Models** — ISCA 2022
  - Repository record: assets/scripts/pub_list/htmls/synergy_2022/paper_scholar2022_themis-a-network-bandwidth-aware-collective-scheduli.html
  - Paper: https://arxiv.org/abs/2110.04478
- **TACOS: Topology-Aware Collective Algorithm Synthesizer for Distributed Machine Learning** — MICRO 2024
  - Repository record: assets/scripts/pub_list/htmls/synergy_2024/paper_scholar2024_tacos-topology-aware-collective-algorithm-synthesize.html
  - Paper: https://scholar.google.com/scholar?oi=bibs&cluster=15651408857113340475&btnI=1&hl=en
- **FRED: A Wafer-scale Fabric for 3D Parallel DNN Training** — ISCA 2025
  - Repository record: assets/scripts/pub_list/htmls/synergy_2025/paper_scholar2025_fred-a-wafer-scale-fabric-for-3d-parallel-dnn-traini.html
  - Paper: https://scholar.google.com/scholar?oi=bibs&cluster=2273571354661174918&btnI=1&hl=en
- **Closing the Efficiency Gap: AI Datacenter Co-design Roadmap for Scalable Training of LLMs** — ICS 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2026/paper_scholar2026_closing-the-efficiency-gap-ai-datacenter-co-design-r.html
  - Paper: https://scholar.google.com/scholar?oi=bibs&cluster=5432467094199458900&btnI=1&hl=en
- **MLCommons Chakra: Advancing Performance Benchmarking and Co-design using Standardized Execution Traces** — MLSys 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2026/paper_scholar2026_mlcommons-chakra-advancing-performance-benchmarking.html
  - Paper: https://arxiv.org/abs/2605.11333

## Interconnects, Memory & Chiplet Systems

- **SWAP: Synchronized Weaving of Adjacent Packets for Network Deadlock Resolution** — MICRO 2019
  - Repository record: assets/scripts/pub_list/htmls/synergy_2019/paper_scholar2019_swap-synchronized-weaving-of-adjacent-packets-for-ne.html
  - Paper: https://www.eecg.utoronto.ca/~enright/swap2019.pdf
- **Kite: A Family of Heterogeneous Interposer Topologies Enabled via Accurate Interconnect Modeling** — DAC 2020
  - Repository record: assets/scripts/pub_list/htmls/synergy_2020/paper_scholar2020_kite-a-family-of-heterogeneous-interposer-topologies.html
  - Paper: https://jiemingyin.github.io/docs/DAC2020.pdf
- **ecoTLB: Eventually Consistent TLBs** — ACM TACO 2020
  - Repository record: assets/scripts/pub_list/htmls/synergy_2020/paper_scholar2020_ecotlb-eventually-consistent-tlbs.html
  - Paper: https://gts3.org/assets/papers/2020/maass%3Aecotlb.pdf
- **TNT: A Modular Approach to Traversing Physically Heterogeneous NoCs at Bare-Wire Latency** — ACM TACO 2023
  - Repository record: assets/scripts/pub_list/htmls/synergy_2023/paper_scholar2023_tnt-a-modular-approach-to-traversing-physically-hete.html
  - Paper: https://scholar.google.com/citations?view_op=view_citation&hl=en&user=P__ztgcAAAAJ&cstart=100&pagesize=100&sortby=pubdate&citation_for_view=P__ztgcAAAAJ:b1wdh0AR-JQC
- **On Continuing DNN Accelerator Architecture Scaling Using Tightly-coupled Compute-on-Memory 3D ICs** — IEEE TVLSI 2023
  - Repository record: assets/scripts/pub_list/htmls/synergy_2023/paper_tong2023_3dics.html
  - Paper: https://ieeexplore.ieee.org/document/10221779
- **MCMComm: Hardware-Software Co-Optimization for End-to-End Communication in Multi-Chip-Modules** — arXiv 2025
  - Repository record: assets/scripts/pub_list/htmls/synergy_2025/paper_scholar2025_mcmcomm-hardware-software-co-optimization-for-end-to.html
  - Paper: https://arxiv.org/abs/2505.00041

## Efficient & Compositional AI Systems

- **XRBench: An Extended Reality (XR) Machine Learning Benchmark Suite for the Metaverse** — MLSys 2023
  - Repository record: assets/scripts/pub_list/htmls/synergy_2023/paper_scholar2023_xrbench-an-extended-reality-xr-machine-learning-benc.html
  - Paper: https://scholar.google.com/citations?view_op=view_citation&hl=en&user=P__ztgcAAAAJ&cstart=100&pagesize=100&sortby=pubdate&citation_for_view=P__ztgcAAAAJ:Z5m8FVwuT1cC
- **GEAR: An Efficient Error Reduction Framework for KV Cache Compression in LLM Inference** — NeurIPS 2024
  - Repository record: assets/scripts/pub_list/htmls/synergy_2024/paper_scholar2024_gear-an-efficient-error-reduction-framework-for-kv-c.html
  - Paper: https://scholar.google.com/scholar?oi=bibs&cluster=8631300155055483091&btnI=1&hl=en
- **CogSys: Efficient and Scalable Neurosymbolic Cognition System via Algorithm-Hardware Co-Design** — HPCA 2025
  - Repository record: assets/scripts/pub_list/htmls/synergy_2025/paper_wan2025cogsys.html
  - Paper: https://ieeexplore.ieee.org/document/10946710
- **ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models** — ICLR 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2025/paper_ramachandran2025thinkv.html
  - Paper: https://arxiv.org/pdf/2510.01290
- **SLM-MUX: Orchestrating Small Language Models for Reasoning** — ICLR 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2025/paper_wang2025slm.html
  - Paper: https://arxiv.org/pdf/2510.05077
- **Compositional AI Beyond LLMs: System Implications of Neuro-Symbolic-Probabilistic Architectures** — ASPLOS 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2026/paper_wang2026compositional.html
  - Paper: https://dl.acm.org/doi/10.1145/3760250.3762235
- **ThunderAgent: A Simple, Fast and Program-Aware Agentic Inference System** — ICML 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2026/paper_scholar2026_thunderagent-a-simple-fast-and-program-aware-agentic.html
  - Paper: https://arxiv.org/abs/2602.13692

## Secure & Private Computing

- **Mitigating Timing-Based NoC Side-Channel Attacks with LLC Remapping** — IEEE CAL 2023
  - Repository record: assets/scripts/pub_list/htmls/synergy_2023/paper_scholar2023_mitigating-timing-based-noc-side-channel-attacks-wit.html
  - Paper: https://scholar.google.com/citations?view_op=view_citation&hl=en&user=P__ztgcAAAAJ&cstart=100&pagesize=100&sortby=pubdate&citation_for_view=P__ztgcAAAAJ:kuK5TVdYjLIC
- **Accurate Low-Degree Polynomial Approximation of Non-polynomial Operators for Fast Private Inference in Homomorphic Encryption** — MLSys 2024
  - Repository record: assets/scripts/pub_list/htmls/synergy_2024/paper_tong2024smartpaf.html
  - Paper: https://arxiv.org/abs/2404.03216
- **Leveraging ASIC AI Chips for Homomorphic Encryption** — HPCA 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2026/paper_scholar2026_leveraging-asic-ai-chips-for-homomorphic-encryption.html
  - Paper: https://scholar.google.com/scholar?oi=bibs&cluster=3706374279726660658&btnI=1&hl=en
- **SCALE: Tackling Communication Bottlenecks in Confidential Distributed Machine Learning** — HPCA 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2026/paper_scholar2026_scale-tackling-communication-bottlenecks-in-confiden.html
  - Paper: https://scholar.google.com/scholar?oi=bibs&cluster=9927071615161498524&btnI=1&hl=en
- **PRIVATAR: Scalable Privacy-Preserving Multi-User VR via Secure Offloading** — MLSys 2026
  - Repository record: assets/scripts/pub_list/htmls/synergy_2026/paper_scholar2026_privatar-scalable-privacy-preserving-multi-user-vr-v.html
  - Paper: https://arxiv.org/abs/2604.17476

## Additional primary references

- MAESTRO project and publication history: https://maestro.ece.gatech.edu/
- ASTRA-sim project and publication history: https://astra-sim.github.io/
- SIGMA metadata and abstract: https://doi.org/10.1109/HPCA47549.2020.00015
- ConfuciuX abstract: https://arxiv.org/abs/2009.02010
- Themis abstract: https://arxiv.org/abs/2110.04478

Descriptions intentionally make no numerical performance or security-guarantee claims beyond the scope of the source papers. Some legacy repository entries contain only titles; the overview uses their documented research topics and primary project/paper sources rather than inventing missing abstracts.
