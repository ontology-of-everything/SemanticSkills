# 开通与退订规范白名单

手工证据快照；不由 `04_generate_docs.py` 生成。`commands.md` 是全量审计候选，本文件记录最终进入 `huawei-cloud-cost-estimation` 的规范主体。

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
- BSS: `CancelResourcesSubscription`（仅统一退订）

合计：73 个开通主体 + 1 个统一退订主体。

## 核验证据

- KooCLI：7.2.2；服务级 help 可发现上述主体。
- 全局本地预演参数为 `--dryrun`：打印请求并跳过业务调用。
- `dry_run` / `dryRun` 是少数接口的服务端请求参数，会访问服务端，不能替代 `--dryrun`。
- BSS 统一退订为 `POST /v2/orders/subscriptions/resources/unsubscribe`；KooCLI 主体是 `BSS CancelResourcesSubscription`。
- 参数与依赖只在运行时 operation help 中解析；本文不保存参数模板。

## 规范化

- `CDN CreateDomain` → `/v1` 与 `/v2`
- 两条 CSS `CreateCluster` → `/v1` 与 `/v2`
- `ELB CreateLoadbalancer/CreateLoadBalancer` → `CreateLoadBalancer/v2` 与 `/v3`
- `MRS CreateCluster` → `/v1` 与 `/v2`
- Kafka 仅保留 `CreatePostPaidKafkaInstance`
- RocketMQ 仅保留 `CreateInstanceByEngine`
- 删除 `GaussDB CreateClickHouseInstance`；当前 KooCLI 不存在，且 StarRocks 不是等价替代

## 已知缺口

- `docs/hcloud` inventory 未覆盖 CDM、CloudTable、CodeArtsInspector、DDM、DeH、ESW、IEC、MetaStudio、SCM；本次只以当前服务级 help 补证，不改全量生成管线。
- CCE `CreateCluster` / `CreateNodePool` 仍有 OPENAPI help 缺口；见 [help-gaps.md](help-gaps.md)。
- CDN 与上述漏收服务的 operation help 在当前环境可能返回 endpoint metadata `Forbidden`。运行时 help 失败时必须停止，不能猜参数。
- `--dryrun` 只证明请求可构造，不证明容量、资格、最终价格、退订影响或退款金额。
