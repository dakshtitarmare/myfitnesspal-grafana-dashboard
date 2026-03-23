import Layout from '../../components/Layout';

const grafanaBaseUrl = process.env.NEXT_PUBLIC_GRAFANA_URL || 'http://localhost:3002';
const grafanaDashboardUrl =
  process.env.NEXT_PUBLIC_GRAFANA_DASHBOARD_URL ||
  `${grafanaBaseUrl}/d/myfitnesspal-overview/myfitnesspal-overview?orgId=1&refresh=30s&kiosk`;

export default function DashboardPage() {
  return (
    <Layout title="Analytics Dashboard">
      <section className="card-grid dashboard-grid">
        <article className="hero-card dashboard-copy">
          <p className="eyebrow">Grafana Embed</p>
          <h2>Live nutrition analytics from PostgreSQL.</h2>
          <p className="lead">
            The embedded dashboard refreshes against the provisioned PostgreSQL datasource and surfaces calorie, macro, and meal-level trends.
          </p>
        </article>
        <div className="grafana-frame-shell">
          <iframe
            title="MyFitnessPal Grafana Dashboard"
            src={grafanaDashboardUrl}
            className="grafana-frame"
            loading="lazy"
            referrerPolicy="strict-origin-when-cross-origin"
          />
        </div>
      </section>
    </Layout>
  );
}
