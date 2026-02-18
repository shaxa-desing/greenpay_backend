def create_tree(db: Session, tree: schemas.TreeCreate):
    db_tree = models.Tree(
        user_id=tree.user_id,
        user_name=tree.user_name,
        tree_type=tree.tree_type,
        location=tree.location,   # 🔥 SHU
        latitude=tree.latitude,
        longitude=tree.longitude
    )
    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)
    return db_tree
