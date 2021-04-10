from typing import Iterable, Set, Tuple

from sqlalchemy.orm import Session

from db_api import models, schemas


def precision_recall_fscore(
    predicted: Set, gold: Set, beta: float = 1.0
) -> Tuple[float, float, float, int, int, int]:
    tp = len(predicted.intersection(gold))
    fp = len(predicted - gold)
    fn = len(gold - predicted)
    precision = tp / (tp + fp + 1e-100)
    recall = tp / (tp + fn + 1e-100)
    fscore = (1 + beta ** 2) * (
        (precision * recall) / (((beta ** 2) * precision) + recall + 1e-100)
    )
    return precision, recall, fscore, tp, fp, fn


def create_ner_evaluation(
    db: Session, ner_evaluation: schemas.NEREvaluationCreate
) -> models.NEREvaluation:
    db_ner_evaluation = models.NEREvaluation(**ner_evaluation.dict())
    db.add(db_ner_evaluation)
    db.commit()
    db.refresh(db_ner_evaluation)
    return db_ner_evaluation


def get_ner_evaluation(db: Session, ner_evaluation_id: int) -> models.NEREvaluation:
    return (
        db.query(models.NEREvaluation)
        .filter(models.NEREvaluation.id == ner_evaluation_id)
        .first()
    )


def get_ner_evaluations(
    db: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.NEREvaluation]:
    return db.query(models.NEREvaluation).offset(skip).limit(limit).all()


def update_ner_evaluation(
    db: Session, ner_evaluation: schemas.NEREvaluationUpdate
) -> models.NEREvaluation:
    new_ner_evaluation = models.NEREvaluation(**ner_evaluation.dict())
    old_ner_evaluation = get_ner_evaluation(db, ner_evaluation.id)
    db.delete(old_ner_evaluation)
    db.add(new_ner_evaluation)
    db.commit()
    db.refresh(new_ner_evaluation)
    return new_ner_evaluation
