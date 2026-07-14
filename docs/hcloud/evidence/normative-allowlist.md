# 开通白名单与退订排除证据

手工证据快照；不由 `04_generate_docs.py` 生成。`commands.md` 是全量审计候选，本文件记录最终进入 `huawei-cloud-cost-estimation` 的开通主体，以及退订接口为何仅保留证据、不进入执行白名单。

## 白名单

- APIG: `CreateInstanceV2`, `CreateOrder`
- BMS: `CreateBareMetalServers`
- CBH: `CreateCbh`, `CreateInstance`, `CreateInstanceOrder`
- CBR: `CreatePolicy`, `CreatePostPaidVault`, `CreateVault`
- CCE: `CreateAutopilotCluster`, `CreateCluster`, `CreateNode`, `CreateNodePool`, `SubscribePackageProducts`
- CDM: `CreateCluster`
- CDN: `CreateDomain/v1`, `CreateDomain/v2`
- CFW: `CreateEastWestFirewall`, `CreateFirewall`
- CloudTable: `CreateCloudTableCluster`, `CreateCluster`
- CloudIDE: `CreateInstance`
- CodeArtsInspector: `CreatePurchaseOrder`
- CSE: `CreateEngine`
- CSS: `CreateCluster/v1`, `CreateCluster/v2`
- DataArtsStudio: `PayForDgcOneKey`
- DBSS: `CreateDbEncryptInstancePeriod`, `CreateDbOmInstancePeriod`, `CreateInstancesPeriodOrder`, `CreateInstancesPeriodOrderNew`
- DCS: `CreateInstance`
- DDM: `CreateDdmInstance`, `CreateInstance`
- DDS: `CreateInstance`
- DeH: `CreateDedicatedHost`
- DSC: `CreateProductOrder`
- DWS: `CreateCluster`, `CreateClusterV2`
- ECS: `CreatePostPaidServers`, `CreateServers`
- EIP: `CreatePrePaidPublicip`, `CreatePublicip`, `CreateSharedBandwidth`
- ELB: `CreateLoadBalancer/v2`, `CreateLoadBalancer/v3`
- EPS: `CreateEnterpriseProject`
- ESW: `CreateInstance`
- EVS: `CreateVolume`
- GaussDB: `CreateGaussMySqlInstance`, `CreateStarrocksInstance`
- GaussDBforNoSQL: `CreateInstance`
- GaussDBforopenGauss: `CreateDatabaseInstance`, `CreateDbInstance`, `CreateGaussDbInstance`, `CreateInstance`
- HSS: `CreateAntiVirusPaidTask`, `CreateQuotasOrder`
- IEC: `CreateInstance`
- Kafka: `CreatePostPaidKafkaInstance`
- MetaStudio: `CreateMetaStudioOrders`
- MRS: `CreateCluster/v1`, `CreateCluster/v2`
- NAT: `CreateNatGateway`
- RabbitMQ: `CreatePostPaidInstanceByEngine`
- RDS: `CreateInstance`, `CreateInstanceIam5`
- RocketMQ: `CreateInstanceByEngine`
- SCM: `SubscribeCertificate`
- SecMaster: `CreateSubscriptionOrder`
- VPN: `CreateVpnServer`
- WAF: `CreateCloudWafPostPaidResource`, `CreateInstance`, `CreatePrepaidCloudWaf`

合计：74 个开通主体；无退订主体。

## 退订排除

KooCLI 可发现 `BSS CancelResourcesSubscription`，对应 `POST /v2/orders/subscriptions/resources/unsubscribe`。该接口不进入技能执行白名单：本地 `--dryrun` 不能展示关联资源、实际退款、手续费与退款流向，技能因此只引导用户在华为云控制台完成退订。

## 核验证据

- KooCLI：7.2.2；服务级 help 可发现上述主体。
- 全局本地预演参数为 `--dryrun`：打印请求并跳过业务调用。
- `dry_run` / `dryRun` 是少数接口的服务端请求参数，会访问服务端，不能替代 `--dryrun`。
- 参数与依赖只在运行时 operation help 中解析；本文不保存参数模板。

## 规范化

- `CDN CreateDomain` → `/v1` 与 `/v2`
- 两条 CSS `CreateCluster` → `/v1` 与 `/v2`
- `ELB CreateLoadbalancer/CreateLoadBalancer` → `CreateLoadBalancer/v2` 与 `/v3`
- `MRS CreateCluster` → `/v1` 与 `/v2`
- CodeArts IDE Online 使用 KooCLI 服务名 `CloudIDE`；仅保留标准用户路径 `CreateInstance`，排除第三方集成路径 `CreateInstanceBy3rd`
- Kafka 仅保留 `CreatePostPaidKafkaInstance`
- RocketMQ 仅保留 `CreateInstanceByEngine`
- 删除 `GaussDB CreateClickHouseInstance`；当前 KooCLI 不存在，且 StarRocks 不是等价替代

## 已知缺口

- `docs/hcloud` inventory 未覆盖 CDM、CloudTable、CloudIDE、CodeArtsInspector、DDM、DeH、ESW、IEC、MetaStudio、SCM；本次只以当前服务级 help 补证，不改全量生成管线。
- CCE `CreateCluster` / `CreateNodePool` 仍有 OPENAPI help 缺口；见 [help-gaps.md](help-gaps.md)。
- CDN 与上述漏收服务的 operation help 在当前环境可能返回 endpoint metadata `Forbidden`。运行时 help 失败时必须停止，不能猜参数。
- `--dryrun` 只证明请求可构造，不证明容量、资格或最终价格；更不能证明退订影响、退款金额和资金流向。
