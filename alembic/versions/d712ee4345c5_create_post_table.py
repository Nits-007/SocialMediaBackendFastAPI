"""create post table

Revision ID: d712ee4345c5
Revises: 
Create Date: 2024-06-18 02:19:36.282509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship



# revision identifiers, used by Alembic.
revision: str = 'd712ee4345c5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts' , 
                    sa.Column('id' , sa.Integer(),nullable=False,primary_key=True) ,
                    sa.Column('title' , sa.String(),nullable=False) ,
                    sa.Column('content' , sa.String() ,nullable=False) ,
                    sa.Column('published' , sa.Boolean() , server_default='True', nullable=False) ,
                    sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , nullable=False , server_default=sa.text('now()')) ,
                    sa.Column('owner_id' , sa.Integer() , sa.ForeignKey("users.id" , ondelete="CASCADE") , nullable=False) ,
                    sa.Column(owner = relationship("User"))
                    )
    pass


def downgrade() :
    op.drop_table("posts")
    pass
