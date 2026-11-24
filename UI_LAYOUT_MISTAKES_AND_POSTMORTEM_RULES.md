# FEAR & HUNGER: TERMINAL LABYRINTH
## BÁO CÁO PHÂN TÍCH TOÀN DIỆN LỖI GIAO DIỆN (UI/LAYOUT POSTMORTEM) VÀ QUY TẮC THIẾT KẾ BẤT BIẾN
*Tài liệu lưu trữ chính thức phục vụ nghiệm thu, đào tạo và quy chuẩn hóa phát triển giao diện Terminal ANSI*

---

### MỤC LỤC
1. [TỔNG QUAN & BỐI CẢNH DỰ ÁN](#1-tổng-quan--bối-cảnh-dự-án)
2. [PHÂN TÍCH CHI TIẾT 10 LỖI LAYOUT QUA ẢNH CHỤP THỰC TẾ](#2-phân-tích-chi-tiết-10-lỗi-layout-qua-ảnh-chụp-thực-tế)
   - [Lỗi 1: Trùng lặp Action Menu, Thừa Dấu Bằng `=====` & Chèn Chữ `[HERO]`](#lỗi-1-trùng-lặp-action-menu-thừa-dấu-bằng--chèn-chữ-hero)
   - [Lỗi 2: Vòng lặp In Header Bất Tận (Endless Header Spam Loop)](#lỗi-2-vòng-lặp-in-header-bất-tận-endless-header-spam-loop)
   - [Lỗi 3: Túi Đồ Dàn Hàng Ngang Bị Cắt Cụt & Huyền Thoại Bản Đồ Chen Chúc](#lỗi-3-túi-đồ-dàn-hàng-ngang-bị-cắt-cụt--huyền-thoại-bản-đồ-chen-chúc)
   - [Lỗi 4: Xếp Chồng Giao Diện Độ Khó Lên Bộ Chọn Hero (Screen Stacking)](#lỗi-4-xếp-chồng-giao-diện-độ-khó-lên-bộ-chọn-hero-screen-stacking)
   - [Lỗi 5: Thanh Điều Khiển & Nhật Ký Dính Chặt Viền Bản Đồ](#lỗi-5-thanh-điều-khiển--nhật-ký-dính-chặt-viền-bản-đồ)
   - [Lỗi 6: Giải Pháp Guide Book Modal Tách Biệt Huyền Thoại Khỏi Map](#lỗi-6-giải-pháp-guide-book-modal-tách-biệt-huyền-thoại-khỏi-map)
   - [Lỗi 7: Cơ Chế Mutilation / Đứt Tứ Chi & Hiệu Ứng Hổ Phách Sylvian](#lỗi-7-cơ-chế-mutilation--đứt-tứ-chi--hiệu-ứng-hổ-phách-sylvian)
   - [Lỗi 8: Cắt Cụt Chuỗi HUD Trên Cùng (`[TRAIT]: Bea`) Do Vượt Quá 100 Cột](#lỗi-8-cắt-cụt-chuỗi-hud-trên-cùng-trait-bea-do-vượt-quá-100-cột)
   - [Lỗi 9: Vỡ Mã Escape ANSI Quái Vật (`30;2;255;255;255m`) Do Cắt Chuỗi Sai](#lỗi-9-vỡ-mã-escape-ansi-quái-vật-302255255255m-do-cắt-chuỗi-sai)
   - [Lỗi 10: Chuẩn Hóa HUD 2 Dòng Phân Cấp Thông Tin Trực Quan](#lỗi-10-chuẩn-hóa-hud-2-dòng-phân-cấp-thông-tin-trực-quan)
3. [SỰ TIẾN HÓA CỦA BỘ CHỌN NHÂN VẬT (3 PHƯƠNG ÁN SONG SONG)](#3-sự-tiến-hóa-của-bộ-chọn-nhân-vật-3-phương-án-song-song)
   - [Thất bại của Ma trận 4x2 cũ (Bóp méo model)](#thất-bại-của-ma-trận-4x2-cũ-bóp-méo-model)
   - [Phương án 1: Ma Trận 4 Ô To Rộng 2x2 (`quad_grid`)](#phương-án-1-ma-trận-4-ô-to-rộng-2x2-quad_grid)
   - [Phương án 2: Bản Dọc Truyền Thống 1 Ô Lớn (`vertical_split`)](#phương-án-2-bản-dọc-truyền-thống-1-ô-lớn-vertical_split)
   - [Phương án 3: Bản Dàn Hàng 3 Cột Khổ Lớn (`panorama_3col`)](#phương-án-3-bản-dàn-hàng-3-cột-khổ-lớn-panorama_3col)
4. [HỆ THỐNG TÚI ĐỒ Ô LƯỚI & CƠ CHẾ TOTEM OF RESTORATION](#4-hệ-thống-túi-đồ-ô-lưới--cơ-chế-totem-of-restoration)
   - [Túi đồ ô lưới 3x2 với Pixel Icon](#túi-đồ-ô-lưới-3x2-với-pixel-icon)
   - [Bảo vật độc nhất: Totem of Flesh Restoration](#bảo-vật-độc-nhất-totem-of-flesh-restoration)
   - [Các hình phạt chấn thương theo thời gian (Bleeding, Agony Mind Loss, Gangrene)](#các-hình-phạt-chấn-thương-theo-thời-gian-bleeding-agony-mind-loss-gangrene)
5. [CÁC QUY TẮC BẤT BIẾN CHO NHÀ PHÁT TRIỂN (DEVELOPMENT INVARIANTS)](#5-các-quy-tắc-bất-biến-cho-nhà-phát-triển-development-invariants)
6. [TIẾN HÓA MỚI: TÚI ĐỒ DUAL SPLIT-BOX VÀ CHUẨN HÓA TIẾNG ANH NGẮN GỌN](#6-tiến-hóa-mới-túi-đồ-dual-split-box-và-chuẩn-hóa-tiếng-anh-ngắn-gọn)
   - [Bất cập của Giao diện Túi đồ cũ (Danh sách đơn điệu không thấy Hero)](#bất-cập-của-giao-diện-túi-đồ-cũ-danh-sách-đơn-điệu-không-thấy-hero)
   - [Thiết kế Hộp Kép Đối Xứng (Dual Split-Box Showcase Architecture)](#thiết-kế-hộp-kép-đối-xứng-dual-split-box-showcase-architecture)
   - [Thanh đo Đồ họa Trực quan (Visual Gauge Bars: HP, Mind, Hunger, Tox)](#thanh-đo-đồ-họa-trực-quan-visual-gauge-bars-hp-mind-hunger-tox)
   - [Chuẩn hóa Tiếng Anh Ngắn gọn (Concise English Localization & Anti-Truncation)](#chuẩn-hóa-tiếng-anh-ngắn-gọn-concise-english-localization--anti-truncation)
   - [Đồng nhất Điểm Khởi Chạy Duy nhất (`PLAY_GAME.bat`)](#đồng-nhất-điểm-khởi-chạy-duy-nhất-play_gamebat)

---

### 1. TỔNG QUAN & BỐI CẢNH DỰ ÁN
Dự án *Fear & Hunger: Terminal Labyrinth* vận hành trên terminal Windows với độ phân giải tiêu chuẩn:
- **Chiều ngang (Width):** Chính xác 100 cột (`cols=100`).
- **Chiều dọc (Height):** Tối đa 35-36 dòng (`lines=36`, vùng hiển thị an toàn $\le 35$ dòng để chống scroll và rung giật).
- **Cơ chế hiển thị:** TrueColor 24-bit ANSI qua kỹ thuật `atomic_blit()` bằng cách đưa con trỏ về `(0, 0)` (`\033[H`) thay vì xóa màn hình `cls` liên tục gây nhấp nháy.

Trong quá trình phát triển nhanh, việc bổ sung liên tiếp các tính năng (Mutilation tứ chi, bảng hướng dẫn Guide Book, HUD chi tiết, combat menu linh hoạt, chọn hero đa dạng) đã làm phát sinh nhiều lỗi bố cục nghiêm trọng. Tài liệu này tổng kết toàn bộ 10 trường hợp lỗi cụ thể từ ảnh chụp của người dùng nhằm rút kinh nghiệm vĩnh viễn cho toàn bộ codebase.

---

### 2. PHÂN TÍCH CHI TIẾT 10 LỖI LAYOUT QUA ẢNH CHỤP THỰC TẾ

#### Lỗi 1: Trùng lặp Action Menu, Thừa Dấu Bằng `=====` & Chèn Chữ `[HERO]`
- **Hiện tượng thực tế:** Trong menu combat, tùy chọn `[3] FLEE` bị in lặp 2 lần, các dòng mô tả lệnh bị dính các chuỗi dấu bằng dài ngoằng vô nghĩa (`=================`). Phía trên mô hình nhân vật Ragnvaldr, chữ `[HERO]` bị in đè trực tiếp lên đỉnh đầu, đẩy nửa trên của sprite lệch lên trên và làm biến dạng khung hình.
- **Nguyên nhân kỹ thuật (Root Cause):**
  1. Menu chọn hành động không có vùng đệm cố định (fixed-slot buffer). Khi người chơi chuyển giữa Menu chính (Attack/Guard/Skill/Item/Flee) và Menu phụ (Chọn mục tiêu chi Head/Torso/Arms/Legs), các chuỗi cũ có độ dài lớn hơn chuỗi mới không được xóa trắng (cleared), dẫn đến việc ký tự thừa (trailing `===`) từ các đường viền trước đó còn lưu lại trên terminal.
  2. Đoạn mã render sprite chèn thêm 1 dòng `[HERO]` trực tiếp vào mảng dòng sprite mà không trừ đi chiều cao tổng thể, làm sprite tăng từ 12 dòng lên 13 dòng, phá vỡ căn chỉnh với khung thông số bên cạnh.
- **Biện pháp khắc phục (Fix):**
  - Chuẩn hóa Menu Combat thành một Frame 6 dòng cố định. Mọi dòng trong menu luôn được format với hàm `fit_exact(text, 98)` để tự động đệm khoảng trắng đến hết viền phải, xóa sạch mọi tàn dư của khung hình trước.
  - Loại bỏ hoàn toàn nhãn `[HERO]` phía trên đỉnh đầu sprite. Chuyển thông tin định danh hero sang khung trạng thái bên phải (`HERO : RAGNVALDR [Outlander Berserker]`).

#### Lỗi 2: Vòng lặp In Header Bất Tận (Endless Header Spam Loop)
- **Hiện tượng thực tế:** Màn hình console bị tràn ngập bởi hàng chục dòng tiêu đề:
  `| FEAR & HUNGER: SOLO SURVIVOR COMBAT ARENA - RAGNVALDR [Outlander Berserker] |` in lặp liên tục, đẩy toàn bộ nội dung quái vật và combat ra khỏi màn hình.
- **Nguyên nhân kỹ thuật (Root Cause):**
  - Khi bắt đầu trận chiến, vòng lặp combat xử lý sự kiện gặp phải vòng lặp `while True:` nhưng không bắt được lệnh dừng (non-blocking read trả về chuỗi rỗng liên tục), trong khi trong vòng lặp lại gọi lệnh `print(header)` thay vì gọi `atomic_blit()`. Mỗi millisecond in ra 1 dòng header khiến màn hình trượt điên cuồng.
- **Biện pháp khắc phục (Fix):**
  - Cấm tuyệt đối lệnh `print()` tự do trong vòng lặp game chính.
  - Toàn bộ khung hình phải được gom vào một mảng `lines = []` hoàn chỉnh (đúng 100 cột, $\le 35$ dòng) và xuất ra màn hình duy nhất 1 lần qua `atomic_blit(lines)`.
  - Sử dụng cơ chế blocking input (`msvcrt.getch()`) để terminal chỉ vẽ lại khi có phím bấm từ người chơi.

#### Lỗi 3: Túi Đồ Dàn Hàng Ngang Bị Cắt Cụt & Huyền Thoại Bản Đồ Chen Chúc
- **Hiện tượng thực tế:** Túi đồ dồn toàn bộ vật phẩm lên 1 dòng duy nhất:
  `[SURVIVAL POUCH]: [1] Poppy Flower x1 (+50 HP) | [2] Marijuana Herb x1 (+120 HP) | [3] Moldy B...`
  Vật phẩm thứ 3 bị cắt đứt ngang xương ở mép phải cột 100. Người chơi phải bấm phím số 1, 2, 3 thiếu trực quan. Phần chú thích map (LEGEND) chiếm hẳn 2 dòng phía dưới, làm màn hình chật chội.
- **Nguyên nhân kỹ thuật (Root Cause):**
  - Coi túi đồ như một chuỗi text phụ trợ ghép bằng dấu gạch đứng `" | ".join(...)` thay vì một giao diện chuyên biệt. Với màn hình 100 cột, mỗi vật phẩm có tên và hiệu ứng dài khoảng 25-30 ký tự, dòng ngang tối đa chỉ chứa được 2 vật phẩm rưỡi trước khi bị tràn.
- **Biện pháp khắc phục (Fix):**
  - Xây dựng giao diện Túi Đồ Ma Trận 3x2 (`demo_grid_inventory.py`) với 6 ô chứa riêng biệt, mỗi ô có biểu tượng pixel art màu sắc, số lượng rõ ràng và điều hướng trực quan bằng W/A/S/D.
  - Chuyển toàn bộ Legend bản đồ sang một màn hình Hướng Dẫn độc lập (`[G] Guide`).

#### Lỗi 4: Xếp Chồng Giao Diện Độ Khó Lên Bộ Chọn Hero (Screen Stacking)
- **Hiện tượng thực tế:** Sau khi người chơi bấm chọn độ khó (Fear & Hunger / Terror & Starvation), menu độ khó không biến mất mà vẫn nằm nguyên ở nửa trên màn hình, menu chọn Hero lại in tiếp nối ở phía dưới, khiến chiều cao vượt quá 45 dòng, gây vỡ bố cục và thanh trượt terminal xuất hiện.
- **Nguyên nhân kỹ thuật (Root Cause):**
  - Thiếu hàm dọn dẹp màn hình chuyển cảnh (Screen Transition Lifecycle). Hàm chọn độ khó kết thúc nhưng không xóa buffer màn hình trước khi gọi hàm chọn nhân vật.
- **Biện pháp khắc phục (Fix):**
  - Tạo quy tắc chuyển cảnh bắt buộc: Mọi hàm kết thúc trạng thái (State Transition) phải gọi `dui.clear_screen()` và reset vị trí con trỏ trước khi gọi trạng thái kế tiếp.

#### Lỗi 5: Thanh Điều Khiển & Nhật Ký Dính Chặt Viền Bản Đồ
- **Hiện tượng thực tế:** Dòng thông báo nhật ký (`[EXPEDITION LOG]`) và thanh phím tắt (`[CONTROLS]`) dính liền vào nhau không có dòng cách, các thông tin sát đặc khiến người chơi rất khó phân biệt giữa thông báo sự kiện cốt truyện và hướng dẫn thao tác phím.
- **Nguyên nhân kỹ thuật (Root Cause):**
  - Thiếu quy chuẩn về khoảng thở trực quan (Visual Breathing Room). Lập trình viên cố nhét tất cả vào 2 dòng cuối cùng mà không có viền ngăn cách phân đoạn.
- **Biện pháp khắc phục (Fix):**
  - Đặt các đường phân cách rõ ràng (`+--------------------+`) giữa phần Log tường thuật sự kiện và thanh phím bấm Controls. Mỗi nhóm thông tin có mã màu riêng: Log dùng màu vàng sáng `\033[1;33m`, Controls dùng màu xám mờ `\033[90m` với phím tắt màu trắng nổi bật.

#### Lỗi 6: Giải Pháp Guide Book Modal Tách Biệt Huyền Thoại Khỏi Map
- **Hiện tượng thực tế & Ý kiến người dùng:** Bảng chú thích các ô màu (Tường xanh, Đá đỏ, Niêm phong tím, Khe nứt vàng, Rương nâu) làm vướng tầm mắt khi đang khám phá hầm ngục. Người dùng yêu cầu chuyển thành một nút bấm gọi ra sách hướng dẫn riêng.
- **Biện pháp khắc phục (Fix):**
  - Đã hiện thực hóa phím tắt `[G] Guide` ngay trên thanh điều khiển.
  - Khi bấm `[G]`, một cửa sổ Popup Guide Book dạng khung hộp (`FEAR & HUNGER: EXPEDITION SURVIVOR GUIDE BOOK`) hiện ra, chia làm 3 phân vùng rõ rệt:
    1. `[LABYRINTH TILES & HAZARDS]`: Ý nghĩa từng ô gạch, quái vật, chướng ngại vật.
    2. `[SURVIVAL SUPPLIES & POUCH]`: Công dụng chi tiết các loài thảo dược, lương khô, rượu bia.
    3. `[CONTROLS]`: Tổng hợp toàn bộ phím tắt di chuyển, túi đồ, hồi máu khẩn cấp.
  - Bấm phím bất kỳ hoặc `[G]`/`[Esc]` sẽ đóng Guide Book và trả lại bản đồ khám phá sạch sẽ 100%.

#### Lỗi 7: Cơ Chế Mutilation / Đứt Tứ Chi & Hiệu Ứng Hổ Phách Sylvian
- **Hiện tượng thực tế & Thử nghiệm:** Nhân vật trong Fear & Hunger phải chịu đựng tổn thương vật lý vĩnh viễn chứ không chỉ là tụt máu đơn thuần. Người dùng yêu cầu tạo mô hình nhân vật bị đứt tay/chân và quy tắc màu hổ phách ở khớp đứt.
- **Hiện tượng đạt được:**
  - Trong ảnh 7, Ragnvaldr bị thương nặng, một cánh tay bị chém đứt, vị trí vết cắt được đánh dấu bằng ánh sáng hổ phách Sylvian (`\033[38;2;230;140;30m`).
  - Toàn bộ 8 nhân vật đã được tạo đủ 3 trạng thái trong `hero_tri_state_catalog.py`:
    1. `normal`: Tư thế sẵn sàng chiến đấu, đầy đủ binh khí và giáp trụ.
    2. `injured`: Mất tay hoặc mất chân, vết thương rỉ máu và phát sáng hổ phách, tư thế xiêu vẹo.
    3. `dead`: Gục ngã trên vũng máu, vũ khí gãy đổ, chuyển sang tông màu xám lạnh chết chóc.

#### Lỗi 8: Cắt Cụt Chuỗi HUD Trên Cùng (`[TRAIT]: Bea`) Do Vượt Quá 100 Cột
- **Hiện tượng thực tế:** Trên thanh thông tin thám hiểm:
  `[EXPLORER]: RAGNVALDR [Outlander Berserker] - HP:128/170 [KEYS]: 2/3 [POS]: (16,16) [TRAIT]: Bea`
  Từ `Beast Gut` bị cắt cụt thô bạo thành `Bea` ở cuối dòng vì độ dài dòng vượt quá 100 ký tự.
- **Nguyên nhân kỹ thuật (Root Cause):**
  - Nhồi nhét toàn bộ thông tin nhân vật (Tên, Class, HP, Keys, Tọa độ, Trait) vào đúng 1 dòng duy nhất. Chiều dài chuỗi tính cả thẻ định dạng vượt qua 108 ký tự, dẫn đến việc bị hàm cắt chuỗi xén bớt phần đuôi.
- **Biện pháp khắc phục (Fix):**
  - Xem chi tiết tại [Lỗi 10](#lỗi-10-chuẩn-hóa-hud-2-dòng-phân-cấp-thông-tin-trực-quan). Tách thành 2 dòng riêng biệt để thông tin có đầy đủ không gian hiển thị.

#### Lỗi 9: Vỡ Mã Escape ANSI Quái Vật (`30;2;255;255;255m`) Do Cắt Chuỗi Sai
- **Hiện tượng thực tế:** Trong trận đánh với Little Drake, mô hình quái vật bị biến dạng nghiêm trọng, in ra các chuỗi ký tự rác như `30;2;255;255;255m` và `2;255;255;255m` ngay giữa thân quái.
- **Nguyên nhân kỹ thuật (Root Cause):**
  - Lỗi cực kỳ nghiêm trọng trong việc xử lý chuỗi ANSI TrueColor: Một hàm định dạng chuỗi đã dùng phương thức cắt chuỗi chuẩn của Python `string[:width]`.
  - Chuỗi TrueColor chứa mã điều khiển `\x1b[38;2;255;255;255m`. Khi hàm cắt chuỗi cắt ngang qua chuỗi này, tiền tố `\x1b[` bị biến mất hoặc tách rời, khiến phần thông số màu phía sau `38;2;255;255;255m` bị coi là ký tự văn bản thông thường và in thẳng lên terminal!
- **Biện pháp khắc phục (Fix):**
  - Xây dựng hàm `fit_exact(s, width)` và `vis_len(s)` bằng Regex `\x1b\[[0-9;]*m`.
  - Thuật toán duyệt từng ký tự: Nếu gặp mã `\x1b`, nó đọc hết toàn bộ token ANSI mà không tăng biến đếm độ rộng hiển thị (`vis_len`). Nhờ đó mã màu luôn nguyên vẹn 100%, không bao giờ bị cắt vụn.

#### Lỗi 10: Chuẩn Hóa HUD 2 Dòng Phân Cấp Thông Tin Trực Quan
- **Hiện tượng thực tế & Thành quả:** Trong ảnh chụp số 10 (màn hình D'Arce), HUD phía trên đã đạt độ hoàn thiện cao nhất:
  - **Dòng 1 (Trạng thái Explorer):** `[EXPLORER]: D'ARCE [Holy Paladin]    HP: 143/155 | MIND: 23/100 | HUNGER: 80/100`
  - **Dòng 2 (Tiến trình Expedition):** `[EXPEDITION]: POS: (23, 3) KEYS: 2/3 SLAIN: 3 STEPS: 116 | TRAIT: Iron Armor (-35% Phys DMG)`
- **Ý nghĩa & Bài học:**
  - Dòng 1 tập trung vào sinh mạng sinh tồn: Máu (HP), Tâm thần (Mind), Đói khát (Hunger).
  - Dòng 2 tập trung vào chiến thuật hầm ngục: Vị trí, Chìa khóa thoát hiểm, Số quái bị diệt, Số bước chân thám hiểm, và Đặc tính giáp trụ đầy đủ không bị mất chữ.

---

### 3. SỰ TIẾN HÓA CỦA BỘ CHỌN NHÂN VẬT (3 PHƯƠNG ÁN SONG SONG)

#### Thất bại của Ma trận 4x2 cũ (Bóp méo model)
- Khi cố gắng nhồi cả 8 nhân vật lên 1 màn hình theo dạng lưới 4 cột x 2 hàng:
  - Chiều ngang màn hình: 100 cột. Chia cho 4 cột chỉ còn $100 / 4 = 24$ ký tự cho mỗi ô.
  - Trong khi đó, mô hình pixel của các nhân vật rộng từ 26 đến 29 cột (ví dụ: Cahara cầm song dao rộng 29 cột, Le'Garde cầm kiếm dài rộng 28 cột).
  - Kết quả: Vũ khí và tay chân của các nhân vật bị cắt cụt, mô hình bị ép lùn xuống chỉ còn 8-9 dòng khiến mất mũ và ủng. Người dùng đánh giá: *"Ma trận 4 đang bị lỗi làm méo mó và mất số lượng"*.

#### Hiện thực hóa 3 Phương án Bố cục Tuyệt đối Không Mất Chi Tiết (`demo_grid_hero_select.py` & `PLAY_GAME.bat`)
Để người chơi tự do lựa chọn trải nghiệm phù hợp nhất, hệ thống đã tích hợp cùng lúc **3 Giao diện Song song**, chuyển đổi tức thì bằng phím **`[TAB]`**:

```
+----------------------------------------------------------------------------------------------------+
|  [TAB] CHUYỂN ĐỔI LINH HOẠT GIỮA 3 PHƯƠNG ÁN GIAO DIỆN (100 CỘT x <= 35 DÒNG)                      |
+----------------------------------------------------------------------------------------------------+
|  Phương án 1: MA TRẬN 4 Ô TO RỘNG 2x2  --> 4 Hero/màn hình, thẻ 48 cột, model 29 cột nguyên vẹn.   |
|  Phương án 2: DỌC TRUYỀN THỐNG 1 Ô LỚN --> Danh sách dọc 30 cột bên trái, sân khấu 67 cột bên phải.|
|  Phương án 3: DÀN HÀNG 3 CỘT KHỔ LỚN   --> 3 Hero/màn hình, thẻ 32 cột, chỉ số 3 dòng thoáng đãng. |
+----------------------------------------------------------------------------------------------------+
```

1. **Phương án 1: Ma Trận 4 Ô To Rộng 2x2 (`quad_grid`):**
   - Thay vì chia 4 cột chật chội, chia làm **2 cột x 2 hàng** (4 hero mỗi trang, 2 trang).
   - Mỗi ô rộng tới **48 cột**: Thoải mái đặt toàn bộ mô hình 29 cột nguyên bản ở bên trái, và 10 dòng chỉ số chi tiết (HP, ATK, DEF, DODGE, Trait, Skill) ở bên phải.
   - Điều khiển 2D mượt mà bằng [W/A/S/D] và các phím số [1-8].

2. **Phương án 2: Bản Dọc Truyền Thống 1 Ô Lớn (`vertical_split`):**
   - Bên trái (30 cột): Menu cuộn dọc hiển thị danh sách 8 nhân vật với con trỏ sáng `▶`.
   - Bên phải (67 cột): "Sân khấu" chính vinh danh hero đang chọn, hiển thị mô hình kích thước cực đại cùng toàn bộ bảng kháng phép, kháng vật lý, và lời bình phẩm sinh tồn độc quyền.

3. **Phương án 3: Bản Dàn Hàng 3 Cột Khổ LỚN (`panorama_3col`):**
   - Chia màn hình thành **3 thẻ lớn (32 cột mỗi thẻ)** trải ngang (3 trang).
   - Mô hình giữ nguyên 100% 29 cột.
   - **Quy tắc cải tiến:** Không dồn 4 chỉ số vào 1 dòng như trước. Tách thành 3 dòng riêng biệt bên dưới chân mô hình:
     - Dòng 1: `HP: 120/120  |  ATK: 32 DMG`
     - Dòng 2: `DEF: 18       |  DODGE: 25%`
     - Dòng 3: `TRAIT: Deep Pockets (2x Capacity)`
   - Cung cấp trải nghiệm so sánh trực quan giữa 3 nhân vật cùng lúc.

---

### 4. HỆ THỐNG TÚI ĐỒ Ô LƯỚI & CƠ CHẾ TOTEM OF RESTORATION

#### Túi đồ ô lưới 3x2 với Pixel Icon (`demo_grid_inventory.py`)
Thay thế hoàn toàn dải túi đồ hàng ngang lỗi thời bằng ma trận 6 ô chiến thuật:
- **Hàng 1 (Vật phẩm y tế & Thần vật):**
  - Ô 1: **TOTEM OF FLESH** (Cổ Thần Bảo Vật Sylvian - Màu Hổ Phách).
  - Ô 2: **POPPY FLOWER** (Hoa Anh Túc - Hồi máu & Cầm máu).
  - Ô 3: **MEDICINAL HERB** (Thảo Dược Y Tế - Thuốc an thần giảm đau đớn).
- **Hàng 2 (Lương thực & Nẹp xương):**
  - Ô 4: **MOLDY BREAD** (Bánh Mì Mốc - Giải cơn đói).
  - Ô 5: **VINTAGE ALE** (Rượu Cổ - Phục hồi Mind, chống điên loạn).
  - Ô 6: **WOOD SPLINT** (Nẹp Gỗ - Cố định xương gãy).

#### Bảo vật độc nhất: Totem of Flesh Restoration
- **Nguồn gốc:** Ý tưởng lấy cảm hứng từ Totem trong Minecraft nhưng được tái định hình theo phong cách tàn khốc của Fear & Hunger.
- **Quy tắc nhận vật phẩm:** Mỗi nhân vật chỉ được cấp duy nhất **1 Totem** vào đầu chuyến thám hiểm; tuyệt đối không thể nhặt thêm hay mua ở bất kỳ đâu trong hầm ngục.
- **Công dụng tối thượng:** Khi kích hoạt, Totem vỡ vụn thành luồng bụi vàng mang tinh chất Sylvia:
  - **Tái sinh toàn bộ tứ chi bị đứt** (chuyển mô hình từ `injured` trở lại `normal`).
  - **Hàn gắn toàn bộ xương gãy** (khôi phục 100% sức tấn công và khả năng né tránh).
  - **Xóa bỏ hoàn toàn trạng thái Chảy máu (Bleeding), Đau đớn cùng cực (Agony), và Hoại tử (Gangrene)**.

#### Các hình phạt chấn thương theo thời gian (Survival Trauma Penalties)
Khi mất tứ chi hoặc gãy xương mà chưa dùng Totem, nhân vật sẽ phải gánh chịu các hiệu ứng suy đồi:
1. **Xuất huyết (Bleeding):** Mỗi 3 bước chân trên bản đồ hoặc mỗi lượt trong combat, nhân vật mất 3-5 HP do máu chảy liên tục từ vết thương hở.
2. **Cơn đau thấu xương (Severe Agony):** Mất tay chân khiến chỉ số Tâm Thần (Mind) tụt 2 điểm sau mỗi bước đi; khi Mind tụt về 0, nhân vật rơi vào trạng thái hoảng loạn tột độ (Panic).
3. **Nhiễm trùng & Hoại tử (Infection & Gangrene):** Sau 40 bước không được cầm máu, vết cắt chuyển sang màu xanh độc địa, độc tố (Toxicity) tăng lên 100%, đe dọa trực tiếp đến tính mạng.

---

### 5. CÁC QUY TẮC BẤT BIẾN CHO NHÀ PHÁT TRIỂN (DEVELOPMENT INVARIANTS)

Để chấm dứt vĩnh viễn các lỗi layout lặp đi lặp lại, mọi dòng code UI trong dự án bắt buộc phải tuân thủ 5 điều răn sau:

1. **Ngân sách 100 Cột & $\le 35$ Dòng (Strict 100x35 Budget):**
   - Mọi dòng xuất ra terminal phải có độ dài hiển thị trực quan (`vis_len`) bằng **chính xác 100 ký tự**. Không bao giờ được phép để 99 hoặc 101 ký tự.
   - Chiều cao toàn bộ khung hình không được vượt quá 35 dòng để bảo đảm không gây ra hiện tượng cuộn màn hình (zero scroll).

2. **Cắt Chuỗi An Toàn Mã Escape (`fit_exact()` Only):**
   - **Tuyệt đối cấm** dùng cú pháp `string[:width]` trên bất kỳ chuỗi nào có chứa mã màu ANSI TrueColor.
   - Luôn luôn dùng hàm chuẩn `fit_exact(text, width)` để bảo toàn tính toàn vẹn của mã màu và tự động bù khoảng trắng cho khung viền.

3. **Vẽ Màn Hình Nguyên Tử (`atomic_blit()` Only):**
   - Cấm dùng nhiều lệnh `print()` rải rác trong vòng lặp game.
   - Toàn bộ màn hình phải được kết xuất thành 1 chuỗi hoàn chỉnh hoặc mảng dòng và ghi ra màn hình trong 1 thao tác duy nhất với con trỏ định vị `\033[H`.

4. **Dọn Sạch Trạng Thái Khi Chuyển Cảnh (Lifecycle Reset):**
   - Mọi thao tác chuyển màn hình (Title -> Select -> Explore -> Combat -> Victory) phải gọi `dui.clear_screen()` trước khi vẽ frame đầu tiên của màn hình mới.

5. **Không Nhồi Nhét Quá Tải (Split Monolithic Lines):**
   - Khi một dòng chứa từ 4 thông số trở lên (như Tên, Class, HP, Keys, Trait...), bắt buộc phải tách đôi thành 2 dòng có phân cấp thị giác rõ ràng, ngăn chặn hoàn toàn nguy cơ tràn dòng và cắt cụt văn bản.

---

### 6. TIẾN HÓA MỚI: TÚI ĐỒ DUAL SPLIT-BOX VÀ CHUẨN HÓA TIẾNG ANH NGẮN GỌN

#### Bất cập của Giao diện Túi đồ cũ (Danh sách đơn điệu không thấy Hero)
- Trong phiên bản trước (như ảnh chụp từ người dùng), khi mở túi đồ sinh tồn (`[I] Pouch`), màn hình chỉ hiển thị một danh sách 8 dòng vật phẩm dạng văn bản đơn giản kèm theo 1 dòng thông số ngắn `[THÁM HIỂM] CAHARA [Mercenary Rogue] | HP: 120/120 | MIND: 63/100 | HUNGER: 80/100 | KEYS: 2/3`.
- **Nhược điểm:**
  1. Người chơi hoàn toàn không quan sát được hình ảnh nhân vật của mình, không thấy rõ hình thái chấn thương (lành lặn hay đứt tay/chân), mất đi tính trực quan nhập vai.
  2. Các chỉ số sinh tồn chỉ hiển thị dưới dạng con số thuần túy, không có thanh đo đồ họa (visual gauge bars) để nhận biết nhanh tình trạng nguy kịch.
  3. Văn bản tiếng Việt dài dễ chạm viền 100 cột và gây khó khăn khi phối hợp trong môi trường quốc tế / open-source.

#### Thiết kế Hộp Kép Đối Xứng (Dual Split-Box Showcase Architecture)
- Để giải quyết triệt để, hệ thống đã tái cấu trúc hàm `build_hero_showcase_boxes()` và `render_pouch_screen()` trong `funger_terminal/demo_grid_inventory.py`:
  - **Khung Trái (46 Cột - Hero Model Showcase):**
    - Đặt mô hình pixel-art 24-bit TrueColor của chính nhân vật đang điều khiển, được căn giữa hoàn hảo (`dui.center_text()`).
    - Phản ánh đúng 3 trạng thái thực tế: Lành lặn (`normal`), Mutilation đứt chi rỉ máu (`injured`), hoặc Gục ngã (`dead`).
  - **Khung Phải (47 Cột - Vitals, Gauges & Limb Status):**
    - Tên, chức nghiệp và trạng thái thể lực.
    - 4 thanh đo màu trực quan có tỷ lệ phần trăm:
      - `HP      :` Thanh xanh lá / đỏ nguy cấp (`[██████████------] 120/120`)
      - `MIND    :` Thanh xanh dương nhạt (`[████████----------]  63/100`)
      - `HUNGER  :` Thanh vàng cảnh báo đói (`[████████████------]  80/100`)
      - `TOXICITY:` Thanh tím báo độc / hoại tử (`[------------------]   0/100`)
    - Chi tiết độ bền 4 chi vật lý: `[HEAD: OK]`, `[TORSO: OK]`, `[ARMS: 2/2]`, `[LEGS: 2/2]`.
    - Đặc tính độc quyền (`TRAIT: Steal & Dual Daggers`).

#### Chuẩn hóa Tiếng Anh Ngắn gọn (Concise English Localization & Anti-Truncation)
- Toàn bộ menu túi đồ sinh tồn, túi đồ tác chiến (Combat Pouch), danh mục vật phẩm và thông báo đã được bản địa hóa sang tiếng Anh ngắn gọn, súc tích:
  - `[RELIC]`: `Auto-revive on death, full HP & restore limbs` ($\le 45$ ký tự).
  - `[HERB]`: `Restores +120 HP & soothes severe pain` ($\le 45$ ký tự).
  - `[RATION]`: `Relieves -40 Hunger (staves off starvation)` ($\le 45$ ký tự).
  - `[TINCTURE]`: `Restores +35 Mind, purges poison & necrosis` ($\le 45$ ký tự).
  - `[KEY]`: `Unlocks Eastern Labyrinth Gate (needs 3 keys)` ($\le 45$ ký tự).
- Độ dài mô tả được khống chế nghiêm ngặt dưới 45 ký tự, đảm bảo khi kết hợp với nhãn vật phẩm và số lượng trong khung 98 cột nội dung, tỷ lệ cắt cụt văn bản (truncation rate) đạt chính xác **0.0%**.

#### Đồng nhất Điểm Khởi Chạy Duy nhất (`PLAY_GAME.bat`)
- Toàn bộ các file `.bat` tạm thời và thử nghiệm riêng lẻ (`SHOW_HERO_MODELS.bat`, `SHOW_MONSTER_MODELS.bat`, `TEST_GRID_HERO_SELECT.bat`, `TEST_GRID_INVENTORY.bat`) đã được loại bỏ hoàn toàn khỏi kho mã nguồn.
- Giữ lại duy nhất **1 file khởi chạy chuẩn:** `PLAY_GAME.bat` tại thư mục gốc của dự án.
- Tự động cấu hình chuẩn `cols=100 lines=36`, kích hoạt VirtualTerminalLevel cho Windows Terminal, tự biên dịch và kiểm tra Verilog RTL nếu có `iverilog`, và khởi động mượt mà bằng Python runtime hoặc VVP hardware simulator.

---
*Tài liệu được biên soạn và chuẩn hóa bởi Antigravity Engine - Retro Game Verilog Lab.*
