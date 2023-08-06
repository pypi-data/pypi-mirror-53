__version__ = '0.5.0'
__title__ = 'hippiepug'
__author__ = 'Bogdan Kulynych'
__email__ = 'hello@bogdankulynych.me'
__copyright__ = '2019 by Bogdan Kulynych (EPFL SPRING Lab)'
__description__ = 'Sublinear-lookup blockchains and efficient key-value Merkle trees with a flexible storage backend'
__url__ = 'https://github.com/spring-epfl/hippiepug'
__license__ = 'MIT'


from .chain import BlockBuilder, Chain
from .tree import TreeBuilder, Tree
from .pack import EncodingParams, encode, decode
