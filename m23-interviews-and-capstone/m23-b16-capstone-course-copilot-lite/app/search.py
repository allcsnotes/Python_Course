from sqlalchemy import text

INDEX = text("""
    update lessons
    set search_vector =
        setweight(to_tsvector('english', title), 'A') ||
        setweight(to_tsvector('english', notes), 'B')
    where id = :id
""")

SEARCH = text("""
    with q as (
        select to_tsquery('english', replace(
            plainto_tsquery('english', :q)::text, '&', '|'
        )) as query
    )
    select l.id as lesson_id, l.code, l.title,
        ts_headline('english', l.notes, q.query, :style)
            as snippet,
        ts_rank_cd(l.search_vector, q.query) as rank
    from lessons l, q
    where l.search_vector @@ q.query
    order by rank desc, l.id
    limit :limit
""")


STYLE = "MaxWords=22, MinWords=12, StartSel=[, StopSel=]"


def index_lesson(session, lesson_id):
    session.execute(INDEX, {"id": lesson_id})


def find(session, query, limit=5):
    rows = session.execute(
        SEARCH, {"q": query, "limit": limit, "style": STYLE}
    ).mappings()
    return [dict(row) for row in rows]
