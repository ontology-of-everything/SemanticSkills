# 生命周期命令白名单

KooCLI 7.2.2 证据快照。这里只保存命令主体与语义；参数必须在执行时通过 `hcloud <Service> <Operation> --help` 获取。

依赖列是查询方向，不代替 help：`P` 项目、`EP` 企业项目、`N` 网络、`AZ` 可用区、`IMG` 镜像、`DISK` 云盘类型、`KEY` 密钥对、`SPEC` 规格、`PRODUCT` 产品、`PARENT` 父资源、`H` 仅以运行时 help 为准。

## 开通命令（73）

| 主体 | 语义 | 计费 | 依赖 |
| --- | --- | --- | --- |
| `APIG/CreateInstanceV2` | 创建专享版实例 | 按需 | P, EP, N |
| `APIG/CreateOrder` | 创建专享版实例订单 | 包周期 | P, EP, N, PRODUCT |
| `BMS/CreateBareMetalServers` | 创建裸金属服务器 | 按需/包周期 | P, EP, N, AZ, IMG, DISK, KEY, SPEC |
| `CBH/CreateCbh` | 创建云堡垒机 | help 决定 | P, EP, N, AZ, SPEC |
| `CBH/CreateInstance` | 创建堡垒机实例 | 按需/包周期 | P, EP, N, AZ |
| `CBH/CreateInstanceOrder` | 创建堡垒机实例订单 | help 决定 | P, PRODUCT |
| `CBR/CreatePolicy` | 创建备份或复制策略 | 非资源订单 | P |
| `CBR/CreatePostPaidVault` | 创建包周期存储库 | 包周期 | P, EP |
| `CBR/CreateVault` | 创建存储库 | help 决定 | P, EP, AZ |
| `CCE/CreateAutopilotCluster` | 创建 Autopilot 集群 | 按需 | P, N, AZ, IMG, SPEC |
| `CCE/CreateCluster` | 创建 CCE 集群 | help 决定 | H |
| `CCE/CreateNode` | 创建集群节点 | 按需/包周期 | P, N, AZ, IMG, DISK, SPEC, PARENT |
| `CCE/CreateNodePool` | 创建节点池 | help 决定 | H |
| `CCE/SubscribePackageProducts` | 订购套餐包 | help 决定 | PRODUCT |
| `CDM/CreateCluster` | 创建 CDM 集群 | help 决定 | H |
| `CDN/CreateDomain/v1` | 创建加速域名 V1 | help 决定 | H |
| `CDN/CreateDomain/v2` | 创建加速域名 V2 | help 决定 | H |
| `CFW/CreateEastWestFirewall` | 创建东西向防火墙 | help 决定 | P, EP |
| `CFW/CreateFirewall` | 创建云防火墙 | 按需/包周期 | P, EP, N, SPEC |
| `CloudTable/CreateCloudTableCluster` | 创建 CloudTable 集群 | help 决定 | H |
| `CloudTable/CreateCluster` | 创建集群 | help 决定 | H |
| `CodeArtsInspector/CreatePurchaseOrder` | 创建购买订单 | help 决定 | H |
| `CSE/CreateEngine` | 创建微服务引擎 | 按需/包周期/免费规格 | P, N, SPEC |
| `CSS/CreateCluster/v1` | 创建 CSS 集群 V1 | 按需/包周期 | P, EP, N, AZ, DISK, SPEC |
| `CSS/CreateCluster/v2` | 创建 CSS 集群 V2 | 按需/包周期 | P, EP, N, AZ, DISK, SPEC |
| `DataArtsStudio/PayForDgcOneKey` | DataArts Studio 一键购买 | help 决定 | H |
| `DBSS/CreateDbEncryptInstancePeriod` | 包周期购买数据库加密实例 | 包周期 | P, EP, N, AZ, IMG, SPEC |
| `DBSS/CreateDbOmInstancePeriod` | 包周期购买数据库运维实例 | 包周期 | P, EP, N, AZ, IMG, SPEC |
| `DBSS/CreateInstancesPeriodOrder` | 创建数据库审计实例（旧接口） | 包周期 | P, EP, N, AZ, IMG, SPEC |
| `DBSS/CreateInstancesPeriodOrderNew` | 创建数据库审计实例 | 包周期 | P, EP, N, AZ, IMG, SPEC |
| `DCS/CreateInstance` | 创建缓存实例 | 按需/包周期 | P, EP, N, SPEC |
| `DDM/CreateDdmInstance` | 创建 DDM 实例 | help 决定 | H |
| `DDM/CreateInstance` | 创建 DDM 实例 | help 决定 | H |
| `DDS/CreateInstance` | 创建文档数据库实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `DeH/CreateDedicatedHost` | 分配专属主机 | help 决定 | H |
| `DSC/CreateProductOrder` | 创建数据安全产品订单 | help 决定 | P, PRODUCT |
| `DWS/CreateCluster` | 创建 DWS 集群 | help 决定 | P, EP, N, AZ, KEY, SPEC |
| `DWS/CreateClusterV2` | 创建 DWS 集群 V2 | help 决定 | P, EP, N, AZ, KEY, SPEC |
| `ECS/CreatePostPaidServers` | 创建按需云服务器 | 按需 | P, EP, N, AZ, IMG, DISK, KEY, SPEC |
| `ECS/CreateServers` | 创建云服务器 | 按需/包周期 | P, EP, N, AZ, IMG, DISK, KEY, SPEC |
| `EIP/CreatePrePaidPublicip` | 申请包周期弹性公网 IP | 包周期 | P, EP |
| `EIP/CreatePublicip` | 申请弹性公网 IP | help 决定 | P, EP |
| `EIP/CreateSharedBandwidth` | 创建共享带宽 | help 决定 | P, EP |
| `ELB/CreateLoadBalancer/v2` | 创建负载均衡器 V2 | help 决定 | P, EP, N |
| `ELB/CreateLoadBalancer/v3` | 创建独享型负载均衡器 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `EPS/CreateEnterpriseProject` | 创建企业项目 | help 决定 | P |
| `ESW/CreateInstance` | 创建 ESW 实例 | help 决定 | H |
| `EVS/CreateVolume` | 创建云硬盘 | 按需/包周期 | P, EP, AZ, IMG, DISK |
| `GaussDB/CreateGaussMySqlInstance` | 创建 TaurusDB 实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `GaussDB/CreateStarrocksInstance` | 创建 StarRocks 实例 | 按需/包周期 | P, N, SPEC |
| `GaussDBforNoSQL/CreateInstance` | 创建 GeminiDB/NoSQL 实例 | 按需/包周期 | P, EP, N, AZ, SPEC, PRODUCT |
| `GaussDBforopenGauss/CreateDatabaseInstance` | 创建数据库实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `GaussDBforopenGauss/CreateDbInstance` | 创建数据库实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `GaussDBforopenGauss/CreateGaussDbInstance` | 通过 IAM5 创建数据库实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `GaussDBforopenGauss/CreateInstance` | 创建数据库实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `HSS/CreateAntiVirusPaidTask` | 创建付费病毒扫描任务 | 付费 | P, EP |
| `HSS/CreateQuotasOrder` | 创建 HSS 配额订单 | 包周期 | P, EP |
| `IEC/CreateInstance` | 创建边缘实例 | help 决定 | H |
| `Kafka/CreatePostPaidKafkaInstance` | 创建 Kafka 实例 | 按需/包周期 | P, EP, N, PRODUCT |
| `MetaStudio/CreateMetaStudioOrders` | 创建 MetaStudio 订单 | help 决定 | H |
| `MRS/CreateCluster/v1` | 创建 MRS 集群 V1 | 按需/包周期 | P, EP, N, DISK |
| `MRS/CreateCluster/v2` | 创建 MRS 集群 V2 | 按需/包周期 | P, EP, N, AZ, KEY |
| `NAT/CreateNatGateway` | 创建公网 NAT 网关 | 按需/包周期 | P, EP, N |
| `RabbitMQ/CreatePostPaidInstanceByEngine` | 创建 RabbitMQ 实例 | 按需/包周期 | P, EP, N, PRODUCT |
| `RDS/CreateInstance` | 创建 RDS 数据库实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `RDS/CreateInstanceIam5` | 通过 IAM5 创建 RDS 实例 | 按需/包周期 | P, EP, N, AZ, SPEC |
| `RocketMQ/CreateInstanceByEngine` | 创建 RocketMQ 实例 | 按需/包周期 | P, EP, N, PRODUCT |
| `SCM/SubscribeCertificate` | 购买 SSL 证书 | help 决定 | H |
| `SecMaster/CreateSubscriptionOrder` | 开通安全云脑订阅 | 按需/包周期 | P, PRODUCT |
| `VPN/CreateVpnServer` | 创建 VPN 服务端 | help 决定 | P, N |
| `WAF/CreateCloudWafPostPaidResource` | 开通云模式按需 WAF | 按需 | P, EP |
| `WAF/CreateInstance` | 创建 WAF 独享引擎实例 | 按需 | P, EP, N, SPEC |
| `WAF/CreatePrepaidCloudWaf` | 购买包周期云模式 WAF | 包周期 | P, EP, PRODUCT |

## 统一退订命令（1）

| 主体 | 语义 | 范围 | 依赖 |
| --- | --- | --- | --- |
| `BSS/CancelResourcesSubscription` | 生成包年/包月资源退订订单 | 不适用于普通按需资源；可能连带计费关联资源 | P, H |

## 依赖查询命令

只读查询也必须先看运行时 help；这里不给参数。

| 标签 | 命令主体 | 语义 |
| --- | --- | --- |
| P | `IAM/KeystoneListAuthProjects`, `IAM/KeystoneListProjects` | 项目范围 |
| EP | `EPS/ListEnterpriseProject` | 企业项目 |
| N | `VPC/ListVpcs/v3`, `VPC/ListSubnets`, `VPC/ListSecurityGroups/v3` | VPC、子网、安全组 |
| AZ | `ECS/NovaListAvailabilityZones`, `ECS/ListServerAzInfo` | 可用区 |
| IMG | `IMS/ListImages` | 镜像 |
| DISK | `EVS/CinderListVolumeTypes` | 云硬盘类型 |
| KEY | `ECS/NovaListKeypairs` | 密钥对 |
| SPEC | `ECS/NovaListFlavors`; 各产品 `ListFlavors` | 当前服务规格 |
| PRODUCT | `Kafka/ListEngineProducts`, `RabbitMQ/ListEngineProducts`, `RocketMQ/ListEngineProducts`, `SecMaster/ListSubscriptionProduct` | 可售产品 |
| PARENT | `CCE/ListClusters` | 目标集群 |
| H | `hcloud <Service> <Operation> --help` | 运行时发现；help 失败即停止 |
