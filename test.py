from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a language model assistant helping a user with a task. The user asks you to summarize the abstract of a paper in Korean. The user will provide the abstract in the next message."},
        {"role": "system", "content": "You are good at summarizing text in Korean, Suggesting easy-to-understand words and phrases, and providing a concise summary."},
        {"role": "user", "content": "Summarize the abstract of the paper that I'll introduce you in following message In Korean."},
        {"role": "assistant", "content": "알겠습니다. 논문의 초록을 소개해주시면 한국어로 요약해드리겠습니다."},
        {"role": "user", "content": "제목:컴퓨터 게임, 디지털 내러티브, 상호작용성\n초록:컴퓨터 게임의 이야기는 이용자의 선택과 수행에 의해 생성된 사건의 배열에 의존하며, 이러한 상호작용적 특징은 기존의 이야기하기 양식과 중요한 차이점을 낳는다. 내러티브는 이야기와 담화의 구조로 논의되며, ‘이야기하기’는 이야기 시간과 담화 시간이라는 이중의 시간구조에 기반한다. 그러나 컴퓨터 게임은 이용자의 구체적인 행위에 의해 현재 시점에서 사건이 발생하기 때문에 이야기 시간과 담화 시간의 차이가 존재하지 않는다. 따라서 시점이나 서술 방식 등 기존의 담화 양식은 그 의미가 퇴색할 수밖에 없다. 즉 상호작용성은 이야기 시간과 담화 시간간의 차이를 허용하지 않음으로써 기존의 담화 양식을 무용화시킨다. 또한 컴퓨터 게임의 공간적 특징을 반영할 수 있는 새로운 이야기하기 양식을 필요로 하는데, 공간적 이야기 구성에 의존하는 컴퓨터 게임에서 이용자의 탐색 행위는 단순한 이동행위가 아니라 일종의 묘사 행위로서의 의미를 가지며, 컴퓨터 게임의 이야기 구성에서 상호작용성과 동시에 서사성을 확보하는 장치가 된다."},
        {"role": "assistant", "content": "해당 논문의 주제는 컴퓨터 게임의 이야기 진행 방식입니다. 해당 논문은 이야기 시간과 담화 시간이라는 이중의 시간구조가, 기존의 \"이야기하기\"에서는 구분되었지만 컴퓨터 게임에서는 구분되지 않는다고 말합니다. 컴퓨터 게임은 이용자의 구체적인 행위에 의해 현재 시점에서 사건이 발생하기 때문에 이야기 시간과 담화 시간의 차이가 사라지는데, 이때 이용자의 탐색 행위가 이야기를 진행시켜 서사성과 상호작용성을 확보함으로써, 컴퓨터 게임은 공간적 이야기 구성을 가지게 됩니다."},
        {"role": "user", "content": "Summarize the abstract of the paper that I'll introduce you in following message In Korean."},
        {"role": "assistant", "content": "알겠습니다. 논문의 초록을 소개해주시면 한국어로 요약해드리겠습니다."},
        {"role": "user", "content": "제목:물리기반 렌더링에서의 비스플라인 볼륨 BRDF 표현과 응용\n초록:Physically-based rendering is an image synthesis technique based on simulation of physical interactions between light and surface materials. Since generated images are highly photorealistic, physicallybased rendering has become an indispensable tool in advanced design visualization for manufacturing and architecture as well as in film VFX and animations. Especially, BRDF (bidirectional reflectance distribution function) is critical in realistic visualization of materials since it models how an incoming light is reflected on the surface in terms of intensity and outgoing angles. In this paper, we introduce techniques to represent BRDF as B-spline volumes and to utilize them in physically-based rendering. We show that B-spline volume BRDF (BVB) representation is suitable for measured BRDFs due to its compact size without quality loss in rendering. Moreover, various CAGD techniques can be applied to B-spline volume BRDFs for further controls such as refinement and blending."},
        {"role": "assistant", "content": "해당 논문의 주제는 양방향 반사 분포함수(BRDF)를 B-spline Volume으로 표현하고 그것을 PBR(Physically-Based Rendering)에 적용하는 것입니다. PBR이 굉장히 사실적이고 VFX와 애니메이션 분야에 널리 쓰일 정도로 중요하지만, 재질의 측정 BRDF를 렌더링하는 데 있어 원시 데이터의 크기가 너무 큰 문제가 있습니다. 해당 논문은 BRDF를 B-spline volume으로 표현함으로써 재질의 BRDF를 렌더링하는 데 있어 원시 데이터의 크기를 줄이고, 렌더링 품질을 유지하는 방법을 제시합니다. 또한, B-spline volume BRDF에 다양한 CAGD 기법을 적용하여 렌더링의 품질을 높이는 방법을 제시합니다."},
        {"role": "user", "content": "Summarize the abstract of the paper that I'll introduce you in following message In Korean."},
        {"role": "assistant", "content": "알겠습니다. 논문의 초록을 소개해주시면 한국어로 요약해드리겠습니다."},
        {"role": "user", "content": "제목:몰입(Flow) 이론을 적용한 진로상담모형\n초록:몰입이론은 원래 창조적인 활동을 하는 사람들이 자신의 일에 몰입할 때 경험하는 현상에 대한 연구로부터 시작되었지만, 현재는 청소년발달이나 스포츠 심리학, 심지어 심리치료분야에까지 널리 영향을 미치고 있다. 본 연구의 목적은 Csikszentmihalyi의 몰입이론을 적용한 진로상담의 모형을 제시하는 것이다. 본 연구에서 제시하는 진로상담 모형은 몰입이론에서 주장하듯이 개인이 일에서 추구하고자 하는 즐거움과 유능함을 동시에 얻는 것이 가 능하다는 전제에서 출발한다. 따라서 기본적으로 내담자가 흥미와 능력이 균형을 이룬 상태인 몰입을 특정한 영역에서 경험하고 그러한 일에서의 경험이 자신의 진로발달 및 진로결정과도 연결될 수 있도록 돕는 것이 진로상담자의 역할이라고 본다. 본 연구의 전반부에서는 몰입이론에 근거한 진로상담이 기존의 진로상담과 구별되는 점을 다음과 같이 기술하였다. 첫째, 본 진로상담 모형에서는 일이 적응의 대상이 아니라 우리 삶에 즐거움을 주는 원천으로 보고 있다. 둘째, 진로상담의 목표는 적응을 넘어 재능의 발달로 확장된다. 셋째, 진로문제는 진로의식의 미성숙과 같은 ‘의식’의 문제가 아니라 ‘일상생활에서 몰입경험의 부재’나 ‘삶의 의미로 통합되지 못한 몰입경험’으로 본다. 따라서 ‘일상 생활에서 실제적인 몰입경험’의 중요성을 강조한다. 끝으로 진로상담이 진로선택을 돕는 것을 넘어서 아직 선택의 기점에 놓이지 않은 내담자들에게도 몰입을 경험하게 하고 그것이 생의 의미와 통합될 수 있도록 돕는 것이 진로상담의 주요 기능으로 보고 있다. 본 연구의 후반부에는 몰입이론을 진로상담에 적용했을 때 진로문제의 유형을 4개로 구분하여 제시했으며, 그 후 이 모형을 사용할 때의 실제 사례를 소개하였다."}
    ]
)

for choice in response.choices:
    print( choice.message.content )