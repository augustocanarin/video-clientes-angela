# Roteiro de montagem (EDL). Tempos em segundos.
R='/home/user/media/raw/'
IMG={
 'altar':'Altar decoração.jpg','bolachas':'Bolachas.jpg','jesus_bolacha':'Detalhes Jesus em efeito Bolacha de gengibre.jpg',
 'equipe':'Equipe principal de montagem.jpg','confeit_entrega':'Nicho Bolachas.jpg','nicho_arv_real':'Nicho instagramável.jpg',
 'pendentes':'Pendentes iluminados.jpg','recep1':'Recepção 1.jpg','shadow':'Shadow Box.jpg','altar2':'altar 2.jpg',
 'confeiteira':'confeiteira.jpg','bolachas_nicho2':'nicho bolachas 2.jpg','feliz_natal':'nicho árvores.jpg','pendentes2':'pendentes 2.jpg',
 'recep2':'recepção 2.jpg','arvore_seca':'Árvore seca e lanterna.jpg','globo_inst':'bastidores 5.jpeg','ia_altar':'Altar IA.png',
 'ia_corredor':'Corredor Cafeteria Iluminado e Festivo.png','biblia':'Detalhe maxi bíblia.png','ia_globo':'Globo IA.png',
 'ia_confeit':'Nicho Confeitaria IA.png','ia_arvores':'Nicho Árvores instagramável IA.png','ia_quiosque':'Quiosque de Biscoitos Feito com Amor.png',
 'ia_recep':'Recepção IA.png'}
V={'i28':'IMG_1928.MOV','i31':'IMG_1931.MOV','i32':'IMG_1932.MOV','i33':'IMG_1933.MOV','i34':'IMG_1934.MOV','i35':'IMG_1935.MOV',
   'i36':'IMG_1936.MOV','i37':'IMG_1937.MOV','b1':'Bastidor 01.mp4','b2':'bastidor 02.mp4','b3':'bastidor 03.mp4',
   'seca':'processo da Arvore seca.mp4','corr':'corredor cafeteria real.mp4'}
TR={'i28':'IMG_1928','i31':'IMG_1931','i32':'IMG_1932','i35':'IMG_1935','i36':'IMG_1936','i37':'IMG_1937','b3':'bastidor 03'}

def img(k,d,m='zin',**kw): return dict(t='img',k=k,d=d,m=m,**kw)
def split(a,b,d,**kw): return dict(t='split',a=a,b=b,d=d,**kw)
def clip(v,a,d,audio='mute',**kw): return dict(t='clip',v=v,a=a,d=d,audio=audio,**kw)
def talk(v,a,b,cuts=(),**kw): return dict(t='talk',v=v,a=a,b=b,cuts=list(cuts),**kw)
# cutaway: (rel_ini, rel_fim, ('img',k,m) | ('clip',v,a))

TEXT_IA_INTRO=("Antes de executar,", "cada ambiente foi imaginado", "com Inteligência Artificial")

SEGS=[
 # ---------- ABERTURA ----------
 img('feliz_natal',1.8,'panlr',fi=0.5,chapter='abertura'),
 img('pendentes',1.5,'zin'), img('shadow',1.5,'zin'), img('bolachas_nicho2',1.5,'panrl'), img('recep2',1.5,'panlr'),
 img('arvore_seca',3.8,'zin',fo=0.4,ov=[('title',0.3,3.8,'Decoração Maxi de Natal','Angelinne Manualidades  ·  Igreja Nações')]),
 talk('i28',1.45,11.6,cuts=[(5.6,10.15,('img','recep1','panlr'))],fi=0.3),
 # ---------- CAP 1 ----------
 talk('i31',0.0,20.4,cuts=[(8.0,13.2,('clip','b3',30.4)),(17.6,20.4,('clip','seca',0.2))],
      ov=[('chapter',0.2,3.6,'Capítulo 1','A ideia e o planejamento')]),
 img('ia_recep',1.9,'panlr',ov=[('chip',0,1.9,'PROJETO · IA'),('card',0.15,8.3,TEXT_IA_INTRO)]),
 img('ia_arvores',1.35,'panrl',ov=[('chip',0,1.35,'PROJETO · IA')]),
 img('ia_confeit',1.35,'panlr',ov=[('chip',0,1.35,'PROJETO · IA')]),
 img('ia_altar',1.35,'panrl',ov=[('chip',0,1.35,'PROJETO · IA')]),
 img('ia_corredor',1.35,'panlr',ov=[('chip',0,1.35,'PROJETO · IA')]),
 img('ia_globo',1.4,'zin',fo=0.3,ov=[('chip',0,1.4,'PROJETO · IA')]),
 # ---------- CAP 2: NICHO DAS ÁRVORES ----------
 img('ia_arvores',2.6,'zin',fi=0.3,ov=[('chapter',0.0,2.6,'Capítulo 2','Os ambientes',1380),('chip',0,2.6,'PROJETO · IA')]),
 talk('i31',21.1,62.6,cuts=[(20.0,25.8,('img','feliz_natal','zin'))],
      ov=[('env',0.0,3.5,'Nicho das Árvores'),('partner',7.2,13.0,'MODELART','Corte a laser')]),
 # ---------- RECEPÇÃO ----------
 img('ia_recep',2.4,'zin',ov=[('env',0.0,2.4,'Recepção'),('chip',0,2.4,'PROJETO · IA')]),
 talk('i32',0.6,30.1,cuts=[(6.4,10.1,('clip','b2',34.0)),(10.1,17.0,('img','biblia','zin')),(17.0,22.4,('clip','b3',29.6)),(22.4,25.2,('img','recep1','panrl'))],
      ov=[('partner',6.6,12.0,'MODELART','Atendimento para todo o Brasil'),('partner',24.6,29.4,'MODELART','Arquivos do projeto disponíveis')]),
 clip('seca',0.0,8.4,audio='amb',ov=[('env',0.0,3.0,'A árvore seca')]),
 img('arvore_seca',3.6,'zin'),
 img('recep2',3.6,'panlr',ov=[('chip',0,3.6,'RESULTADO')]),
 # ---------- CONFEITARIA ----------
 img('ia_confeit',2.4,'zin',ov=[('env',0.0,2.4,'Nicho Confeitaria'),('chip',0,2.4,'PROJETO · IA')]),
 clip('i33',0.6,4.6,audio='amb'),
 img('confeit_entrega',2.4,'zin'), img('confeiteira',2.2,'panlr'),
 clip('i34',0.0,3.0,audio='amb'),
 img('bolachas_nicho2',2.6,'panrl',ov=[('chip',0,2.6,'RESULTADO')]),
 # ---------- ALTAR ----------
 img('ia_altar',2.4,'zin',ov=[('env',0.0,2.4,'Altar'),('chip',0,2.4,'PROJETO · IA')]),
 talk('i35',0.5,26.1,cuts=[(20.9,25.6,('img','altar2','zin'))],
      ov=[('partner',13.2,19.0,'STEIGLEDER TÊXTIL','Decortela')]),
 img('pendentes',2.6,'zin'), img('pendentes2',2.2,'panlr',ov=[('chip',0,2.2,'RESULTADO')]),
 # ---------- SHADOW BOX ----------
 talk('i36',0.6,24.27,ov=[('env',0.0,3.5,'Shadow Box'),('partner',10.4,16.4,'MODELART','Corte a laser em papelão'),('note',17.8,22.6,'3 m de largura × 2,5 m de altura')]),
 talk('i36',26.75,30.2),
 img('shadow',2.6,'zin',ov=[('chip',0,2.6,'RESULTADO')]),
 # ---------- CORREDOR / GLOBO ----------
 img('ia_corredor',2.2,'zin',ov=[('env',0.0,2.2,'Corredor da Cafeteria'),('chip',0,2.2,'PROJETO · IA')]),
 clip('corr',5.0,3.6),
 img('ia_globo',2.0,'zin',ov=[('chip',0,2.0,'PROJETO · IA')]),
 img('globo_inst',1.7,'zin'),
 clip('corr',0.0,2.3,fo=0.3),
 # ---------- CAP 3: BASTIDORES ----------
 clip('b2',0.0,3.0,audio='amb',fi=0.3,ov=[('chapter',0.0,3.0,'Capítulo 3','Os bastidores')]),
 clip('b2',15.0,2.6,audio='amb'),
 clip('b2',34.6,3.0,audio='amb',ov=[('partner',0.2,2.9,'MODELART','Peças cortadas a laser')]),
 clip('b3',0.0,3.4,audio='amb'), clip('b3',36.6,3.0,audio='amb'), clip('b3',48.4,3.4,audio='amb'),
 talk('b3',62.9,67.45),
 img('equipe',3.2,'zin',fo=0.3,ov=[('note',0.3,3.2,'Equipe de voluntários')]),
 # ---------- CAP 4: TRANSFORMAÇÃO ----------
 split('ia_arvores','nicho_arv_real',3.0,fi=0.3,ov=[('pair',0,3.0),('chapter',0.0,3.0,'Capítulo 4','Do projeto à realidade')]),
 split('ia_recep','recep2',2.7,ov=[('pair',0,2.7)]), split('ia_confeit','bolachas_nicho2',2.7,ov=[('pair',0,2.7)]), split('ia_altar','altar',2.9,fo=0.3,ov=[('pair',0,2.9)]),
 # ---------- CAP 5: RESULTADO ----------
 img('jesus_bolacha',2.6,'zin',fi=0.3,ov=[('chapter',0.0,2.6,'Capítulo 5','O resultado')]),
 img('biblia',2.4,'zin'), img('nicho_arv_real',2.6,'zin',fo=0.3),
 # ---------- ENCERRAMENTO ----------
 img('equipe',4.8,'zout',fi=0.3,ov=[('card',0.2,4.8,("Grandes ideias não precisam","começar com grandes orçamentos.",""))]),
 talk('i37',0.0,11.75),
 img('recep2',3.9,'zin',fo=1.0,ov=[('end',0.2,3.9)]),
]
