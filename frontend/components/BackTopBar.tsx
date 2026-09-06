import Link from "next/link";

export default function BackTopBar({
  title,
  backHref = "/home",
  rightIcon,
  rightHref,
}: {
  title: string;
  backHref?: string;
  rightIcon?: string;
  rightHref?: string;
}) {
  return (
    <div className="topbar-app">
      <Link href={backHref} className="icon-btn" aria-label="Back">
        ←
      </Link>
      <div className="brand">
        <div className="name" style={{ fontSize: 15 }}>
          {title}
        </div>
      </div>
      {rightIcon ? (
        rightHref ? (
          <Link href={rightHref} className="icon-btn">
            {rightIcon}
          </Link>
        ) : (
          <div className="icon-btn">{rightIcon}</div>
        )
      ) : (
        <div style={{ width: 36 }} />
      )}
    </div>
  );
}
