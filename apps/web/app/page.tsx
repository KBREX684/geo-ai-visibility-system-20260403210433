const cards = [
  { title: "定位", value: "AI 可见性运营系统", note: "不承诺排名或必被推荐" },
  { title: "核心交付", value: "GEO Score + 证据链", note: "周跟踪 + 月复盘" },
  { title: "模型策略", value: "GPT-4o 默认可切换", note: "配置驱动，不写死模型" },
  { title: "采集策略", value: "手动 + API 混合", note: "Google AIO 先手工录入" }
];

export default function HomePage() {
  return (
    <main className="container">
      <section className="hero">
        <h1>GEO AI Visibility Console</h1>
        <p>
          用于内部交付的运营后台，覆盖客户 intake、诊断分析、内容生产、排期运营、周报月报、合规校验。
        </p>
      </section>
      <section className="grid">
        {cards.map((card) => (
          <article className="card" key={card.title}>
            <h3>{card.title}</h3>
            <p>{card.value}</p>
            <p className="muted">{card.note}</p>
          </article>
        ))}
      </section>
    </main>
  );
}

