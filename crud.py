from sqlalchemy.orm import Session
import models
import schemas

def create_tree(db: Session, tree: schemas.Tree):

    db_tree = models.Tree(**tree.dict())

    db.add(db_tree)
    db.commit()
    db.refresh(db_tree)

    return db_tree


def get_trees(db: Session):

    return db.query(models.Tree).all()
