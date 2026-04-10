import NavBar from './NavBar'
import SideNav from './SideNav'
import TrendingJobs from './TrendingJobs'
import { Link } from 'react-router-dom'

export default function Layout({ children, rightSidebar }) {
  return (
    <>
      <NavBar />
      <div className="app-layout">
        <aside className="sidebar-left">
          <SideNav />
        </aside>

        <main className="feed-main">
          {children}
        </main>

        <aside className="sidebar-right">
          {rightSidebar || (
            <>
              <TrendingJobs />
              <div className="footer-links">
                <Link to="/privacy">Privacy</Link> ·{' '}
                <Link to="/terms">Terms</Link> ·{' '}
                <Link to="/pricing">Pricing</Link> ·{' '}
                <Link to="/contact">Contact</Link>
                <br />© 2026 Kenya Teaching Vacancies
              </div>
            </>
          )}
        </aside>
      </div>
    </>
  )
}
